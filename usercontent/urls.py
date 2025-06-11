from django.urls import path
from . import views
from .views import ShelfListCreateView, ShelfDetailView

app_name = 'usercontent'

urlpatterns = [
    path('liked-books/', views.LikedBookListCreate.as_view(), name='likedbook-list'),
    path('liked-books/<int:pk>/', views.LikedBookDetail.as_view(), name='likedbook-detail'),

    path('reviews/', views.ReviewListCreate.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),

    path('quotes/', views.QuoteListCreate.as_view(), name='quote-list'),
    path('quotes/<int:pk>/', views.QuoteDetail.as_view(), name='quote-detail'),

    path('shelves/', ShelfListCreateView.as_view(), name='shelf-list'),
    path('shelves/<int:pk>/', ShelfDetailView.as_view(), name='shelf-detail'),

]
