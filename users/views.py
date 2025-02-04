from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer


class SignupView(CreateAPIView):
    """Handles user registration."""
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]  # Allow anyone to sign up





class LogoutView(APIView):
    """Handles user logout by blacklisting the refresh token."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"message": "Successfully logged out"}, status=200)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=400)


class UserProfileView(RetrieveUpdateAPIView):
    """Allows users to view and update their profile."""
    serializer_class = SignupSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # Return the logged-in user


User = get_user_model()


class FollowUserView(APIView):
    """Allows users to follow another user."""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_follow = User.objects.get(id=user_id)
            if request.user == user_to_follow:
                return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

            request.user.following.add(user_to_follow)
            return Response({"message": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UnfollowUserView(APIView):
    """Allows users to unfollow another user."""
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)

            if request.user == user_to_unfollow:
                return Response({"error": "You cannot unfollow yourself"}, status=status.HTTP_400_BAD_REQUEST)

            if not request.user.following.filter(id=user_to_unfollow.id).exists():
                return Response({"error": "You are not following this user"}, status=status.HTTP_400_BAD_REQUEST)

            request.user.following.remove(user_to_unfollow)
            return Response({"message": f"You have unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class FollowerListView(APIView):
    """Returns a list of users who follow the given user."""
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            followers = user.followers.all()
            follower_data = [{"id": u.id, "username": u.username, "bio": u.bio, "profile_picture": u.profile_picture.url if u.profile_picture else None} for u in followers]

            return Response(follower_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class FollowingListView(APIView):
    """Returns a list of users that the given user is following."""
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            following = user.following.all()
            following_data = [{"id": u.id, "username": u.username, "bio": u.bio, "profile_picture": u.profile_picture.url if u.profile_picture else None} for u in following]

            return Response(following_data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
