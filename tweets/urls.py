from django.urls import path
from .views import TweetListCreateView, TweetDetailView, LikeTweetView, CommentListCreateView, CommentDetailView, PersonalizedFeedView

urlpatterns = [
    path('tweets/', TweetListCreateView.as_view(), name='tweet-list'),
    path('tweets/<int:pk>/', TweetDetailView.as_view(), name='tweet-detail'),
    path('tweets/<int:tweet_id>/like/', LikeTweetView.as_view(), name='like-tweet'),
    path('tweets/<int:tweet_id>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('feed/', PersonalizedFeedView.as_view(), name='personalized-feed'),
]
