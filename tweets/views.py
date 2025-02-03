from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tweet, Like, Comment
from .serializers import TweetSerializer, CommentSerializer


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
            return Response({"message": "Tweet liked"}, status=status.HTTP_201_CREATED)
        else:
            like.delete()  # Unlike if already liked
            return Response({"message": "Tweet unliked"}, status=status.HTTP_200_OK)


# -------------------------- COMMENTS CRUD --------------------------

class CommentListCreateView(ListCreateAPIView):
    """Allows users to view all comments and post new ones."""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Fetch comments for a specific tweet."""
        tweet_id = self.kwargs.get('tweet_id')
        return Comment.objects.filter(tweet_id=tweet_id)

    def perform_create(self, serializer):
        """Automatically assign the tweet and user to the comment."""
        try:
            tweet = Tweet.objects.get(id=self.kwargs.get('tweet_id'))
        except Tweet.DoesNotExist:
            raise PermissionDenied("Tweet does not exist.")

        serializer.save(user=self.request.user, tweet=tweet)  # Assign tweet automatically



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
