from django.db import models
from django.conf import settings

class Tweet(models.Model):
    """Model for tweets."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tweets")
    content = models.TextField(max_length=280)  # Max 280 characters
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def likes_count(self):
        """Returns the number of likes on this tweet."""
        return self.likes.count()

    def comments_count(self):
        """Returns the number of comments on this tweet."""
        return self.comments.count()

    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"


class Like(models.Model):
    """Model for likes on tweets."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} liked {self.tweet.id}"


class Comment(models.Model):
    """Model for comments on tweets, now supports nested replies."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name="replies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} commented on {self.tweet.id}"

