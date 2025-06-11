from rest_framework import serializers

from users.serializers import UserSerializer
from .models import LikedBook, Review, Quote, ShelfBook, Shelf


class LikedBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikedBook
        fields = ['id', 'gutenberg_id', 'added_at']

class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'gutenberg_id', 'rating', 'text', 'created_at', 'user']

class QuoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Quote
        fields = ['id', 'gutenberg_id', 'text', 'page_reference', 'created_at', 'user']

class ShelfBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShelfBook
        fields = ['id', 'gutenberg_id']

class ShelfSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()
    book_ids = serializers.ListField(
        child=serializers.IntegerField(), write_only=True, required=False
    )

    class Meta:
        model = Shelf
        fields = ['id', 'name', 'books', 'book_ids']

    def get_books(self, obj):
        return list(obj.shelf_books.values_list('gutenberg_id', flat=True))

    def create(self, validated_data):
        book_ids = validated_data.pop('book_ids', [])
        shelf = Shelf.objects.create(**validated_data)
        for book_id in book_ids:
            ShelfBook.objects.create(shelf=shelf, gutenberg_id=book_id)
        return shelf

    def update(self, instance, validated_data):
        book_ids = validated_data.pop('book_ids', None)
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        if book_ids is not None:
            instance.shelf_books.all().delete()
            for book_id in book_ids:
                ShelfBook.objects.create(shelf=instance, gutenberg_id=book_id)
        return instance

