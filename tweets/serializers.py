from rest_framework import serializers
from .models import Tweet

class TweetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show username instead of ID

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'content', 'created_at', 'updated_at']
