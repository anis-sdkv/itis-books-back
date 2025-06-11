from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import LikedBook, Review, Quote, Shelf
from .serializers import LikedBookSerializer, ReviewSerializer, QuoteSerializer, ShelfSerializer


class BookUserContent(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, gutenberg_id):
        reviews = Review.objects.filter(gutenberg_id=gutenberg_id)
        quotes = Quote.objects.filter(gutenberg_id=gutenberg_id)
        likes_count = LikedBook.objects.filter(gutenberg_id=gutenberg_id).count()

        return Response({
            'reviews':    ReviewSerializer(reviews, many=True).data,
            'quotes':     QuoteSerializer(quotes, many=True).data,
            'likes_count': likes_count,
        })

class LikedBookListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikedBookSerializer

    def get_queryset(self):
        return LikedBook.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LikedBookDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LikedBookSerializer

    def get_queryset(self):
        return LikedBook.objects.filter(user=self.request.user)

class ReviewListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

class QuoteListCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuoteSerializer

    def get_queryset(self):
        return Quote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class QuoteDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = QuoteSerializer

    def get_queryset(self):
        return Quote.objects.filter(user=self.request.user)

class ShelfListCreateView(generics.ListCreateAPIView):
    serializer_class = ShelfSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Shelf.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ShelfDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ShelfSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Shelf.objects.filter(user=self.request.user)

