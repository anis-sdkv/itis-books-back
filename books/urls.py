from django.urls import path

from usercontent.views import BookUserContent
from . import views

app_name = 'books'

urlpatterns = [
    # Книги
    path('', views.BookListView.as_view(), name='book-list'),
    path('<int:gutenberg_id>/', views.BookDetailView.as_view(), name='book-detail'),
    path('popular/', views.popular_books, name='popular-books'),
    path('search/', views.search_books, name='search-books'),

    # Авторы
    path('authors/', views.PersonListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.PersonDetailView.as_view(), name='author-detail'),
    path('authors/popular/', views.popular_authors, name='popular-authors'),

    # Статистика
    path('stats/', views.stats, name='stats'),

    path(
        '<int:gutenberg_id>/content/',
        BookUserContent.as_view(),
        name='book-user-content'
    ),
    path('<int:gutenberg_id>/epub/', views.download_epub, name='book-download-epub'),
]
