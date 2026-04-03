from rest_framework import serializers
from .models import Search, Post

class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Search
        fields = ['id', 'title', 'search_terms']

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'reddit_id', 'created', 'title', 'url', 'img_url', 'body']