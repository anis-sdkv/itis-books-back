from django.urls import path
from . import views
from .views import BookUserContent

app_name = 'usercontent'

urlpatterns = [
    path(
        'books/<int:gutenberg_id>/content/',
        BookUserContent.as_view(),
        name='book-user-content'
    ),

    path('liked-books/', views.LikedBookListCreate.as_view(), name='likedbook-list'),
    path('liked-books/<int:pk>/', views.LikedBookDetail.as_view(), name='likedbook-detail'),

    path('reviews/', views.ReviewListCreate.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),

    path('quotes/', views.QuoteListCreate.as_view(), name='quote-list'),
    path('quotes/<int:pk>/', views.QuoteDetail.as_view(), name='quote-detail'),
]
