from rest_framework import serializers
from .models import Tweet, Like, Comment


class TweetSerializer(serializers.ModelSerializer):
    """Serializer for displaying tweets with likes and comments count."""
    user = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)  # More efficient way to count likes
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)  # More efficient for comments

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'content', 'likes_count', 'comments_count', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    """Serializer for likes."""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Like
        fields = ['id', 'user', 'tweet', 'created_at']


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comments."""
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']
        extra_kwargs = {'tweet': {'required': False}}  # Ensure 'tweet' is not required

