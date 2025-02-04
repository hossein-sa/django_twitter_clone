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


class Notification(models.Model):
    """Model to store notifications for user interactions."""
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('reply', 'Reply'),
        ('follow', 'Follow')
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sent_notifications")
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Track if notification is read

    def __str__(self):
        return f"{self.sender.username} {self.notification_type} notification for {self.user.username}"