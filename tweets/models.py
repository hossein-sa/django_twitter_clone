from django.db import models
from django.conf import settings

class Tweet(models.Model):
    """Model for tweets."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tweets")
    content = models.TextField(max_length=280)  # Max 280 characters
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
