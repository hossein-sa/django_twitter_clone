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
    """Serializer for comments, including nested replies."""
    user = serializers.StringRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'parent', 'replies', 'created_at', 'updated_at']
        extra_kwargs = {'tweet': {'required': False}}  # Ensure 'tweet' is not required

    def get_replies(self, obj):
        """Retrieve replies for a comment."""
        replies = obj.replies.all()
        return CommentSerializer(replies, many=True).data

    def validate(self, data):
        """Ensure a reply belongs to the same tweet as its parent comment."""
        if data.get("parent"):
            if data["parent"].tweet != data["tweet"]:
                raise serializers.ValidationError("Replies must be on the same tweet as the parent comment.")
        return data


