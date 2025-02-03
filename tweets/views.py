from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from .models import Tweet
from .serializers import TweetSerializer

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
