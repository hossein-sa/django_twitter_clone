from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import SignupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from .serializers import SignupSerializer
from .models import CustomUser

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