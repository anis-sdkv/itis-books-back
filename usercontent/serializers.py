from rest_framework import serializers
from .models import LikedBook, Review, Quote

class LikedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedBook
        fields = ['id', 'gutenberg_id', 'added_at']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'gutenberg_id', 'rating', 'text', 'created_at']

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'gutenberg_id', 'text', 'page_reference', 'created_at']
