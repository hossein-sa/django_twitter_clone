from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tweet, Like, Comment, Notification
from .serializers import TweetSerializer, CommentSerializer, NotificationSerializer


# -------------------------- TWEETS CRUD --------------------------

class TweetListCreateView(ListCreateAPIView):
    """Allows users to view all tweets and post new ones."""
    queryset = Tweet.objects.all().order_by('-created_at')
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Assign the logged-in user to the tweet."""
        serializer.save(user=self.request.user)


class TweetDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific tweet."""
    queryset = Tweet.objects.all()
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """Ensure only the tweet owner can edit."""
        if self.get_object().user != self.request.user:
            raise PermissionDenied("You can only edit your own tweets.")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure only the tweet owner can delete."""
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own tweets.")
        instance.delete()


# -------------------------- LIKES --------------------------

class LikeTweetView(APIView):
    """Allows users to like/unlike a tweet."""
    permission_classes = [IsAuthenticated]

    def post(self, request, tweet_id):
        """Like or unlike a tweet."""
        try:
            tweet = Tweet.objects.get(id=tweet_id)
        except Tweet.DoesNotExist:
            return Response({"error": "Tweet not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.get_or_create(user=request.user, tweet=tweet)

        if created:
            # Create a notification for the tweet owner
            Notification.objects.create(
                user=tweet.user,
                sender=request.user,
                notification_type='like',
                tweet=tweet
            )
            return Response({"message": "Tweet liked"}, status=status.HTTP_201_CREATED)
        else:
            like.delete()  # Unlike if already liked
            return Response({"message": "Tweet unliked"}, status=status.HTTP_200_OK)



# -------------------------- COMMENTS CRUD --------------------------

class CommentListCreateView(ListCreateAPIView):
    """Allows users to view and post comments (including replies)."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Fetch top-level comments for a tweet."""
        tweet_id = self.kwargs.get('tweet_id')
        return Comment.objects.filter(tweet_id=tweet_id, parent__isnull=True)

    def perform_create(self, serializer):
        """Assign the tweet and user to the comment, allow replies."""
        try:
            tweet = Tweet.objects.get(id=self.kwargs.get('tweet_id'))
        except Tweet.DoesNotExist:
            raise PermissionDenied("Tweet does not exist.")

        parent_id = self.request.data.get("parent")
        parent_comment = None
        if parent_id:
            try:
                parent_comment = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                raise PermissionDenied("Parent comment does not exist.")

            # Create a notification for the original commenter
            Notification.objects.create(
                user=parent_comment.user,
                sender=self.request.user,
                notification_type='reply',
                comment=parent_comment
            )

        serializer.save(user=self.request.user, tweet=tweet, parent=parent_comment)





class CommentDetailView(RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a specific comment."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """Ensure only the comment owner can edit."""
        if self.get_object().user != self.request.user:
            raise PermissionDenied("You can only edit your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        """Ensure only the comment owner can delete."""
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()

class PersonalizedFeedView(ListAPIView):
    """Shows tweets from users that the logged-in user follows."""
    serializer_class = TweetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        followed_users = self.request.user.following.values_list('id', flat=True)
        return Tweet.objects.filter(user_id__in=followed_users).order_by('-created_at')



class NotificationListView(ListAPIView):
    """Fetches all notifications for the logged-in user."""
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class MarkNotificationAsReadView(APIView):
    """Marks a notification as read."""
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({"error": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)
