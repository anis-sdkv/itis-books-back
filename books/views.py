from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q, Count
from .models import Book, Person
from .serializers import (
    BookListSerializer,
    BookDetailSerializer,
    PersonSerializer,
    PersonDetailSerializer
)


class BookListView(generics.ListAPIView):
    """
    API для получения списка книг с фильтрацией и поиском

    Параметры:
    - search: поиск по названию и автору
    - author: фильтр по ID автора
    - language: фильтр по коду языка
    - subject: фильтр по ID тематики
    - ordering: сортировка (title, download_count, -download_count)
    """
    queryset = Book.objects.all().prefetch_related(
        'authors', 'languages'
    ).select_related()
    serializer_class = BookListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'authors__name']
    ordering_fields = ['title', 'download_count']
    ordering = ['-download_count']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтр по автору
        author_id = self.request.query_params.get('author')
        if author_id:
            queryset = queryset.filter(authors__id=author_id)

        # Фильтр по языку
        language = self.request.query_params.get('language')
        if language:
            queryset = queryset.filter(languages__code=language)

        # Фильтр по тематике
        subject_id = self.request.query_params.get('subject')
        if subject_id:
            queryset = queryset.filter(subjects__id=subject_id)

        return queryset.distinct()


class BookDetailView(generics.RetrieveAPIView):
    """
    API для получения детальной информации о книге
    """
    queryset = Book.objects.all().prefetch_related(
        'authors', 'translators', 'languages', 'subjects',
        'bookshelves', 'formats'
    )
    serializer_class = BookDetailSerializer
    lookup_field = 'gutenberg_id'


class PersonListView(generics.ListAPIView):
    """
    API для получения списка авторов с поиском

    Параметры:
    - search: поиск по имени
    - ordering: сортировка по имени (name, -name)
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']


class PersonDetailView(generics.RetrieveAPIView):
    """
    API для получения детальной информации об авторе
    """
    queryset = Person.objects.all().prefetch_related(
        'authored_books__authors',
        'authored_books__languages',
        'translated_books__authors',
        'translated_books__languages'
    )
    serializer_class = PersonDetailSerializer


@api_view(['GET'])
def popular_books(request):
    """
    API для получения популярных книг (топ по скачиваниям)

    Параметры:
    - limit: количество книг (по умолчанию 10)
    """
    limit = int(request.query_params.get('limit', 10))
    books = Book.objects.filter(
        download_count__isnull=False
    ).prefetch_related(
        'authors', 'languages'
    ).order_by('-download_count')[:limit]

    serializer = BookListSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def popular_authors(request):
    """
    API для получения популярных авторов (по суммарному количеству скачиваний их книг)

    Параметры:
    - limit: количество авторов (по умолчанию 10)
    """
    limit = int(request.query_params.get('limit', 10))
    authors = Person.objects.annotate(
        total_downloads=Count('authored_books__download_count'),
        books_count=Count('authored_books')
    ).filter(
        books_count__gt=0
    ).order_by('-total_downloads')[:limit]

    serializer = PersonSerializer(authors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_books(request):
    """
    Расширенный поиск книг

    Параметры:
    - q: поисковый запрос
    - author: имя автора
    - title: название книги
    - language: язык книги
    """
    query = request.query_params.get('q', '')
    author = request.query_params.get('author', '')
    title = request.query_params.get('title', '')
    language = request.query_params.get('language', '')

    books = Book.objects.all().prefetch_related('authors', 'languages')

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(authors__name__icontains=query)
        )

    if author:
        books = books.filter(authors__name__icontains=author)

    if title:
        books = books.filter(title__icontains=title)

    if language:
        books = books.filter(languages__code__iexact=language)

    books = books.distinct().order_by('-download_count')[:50]  # Лимит 50 результатов

    serializer = BookListSerializer(books, many=True)
    return Response({
        'count': books.count(),
        'results': serializer.data
    })


@api_view(['GET'])
def stats(request):
    """
    API для получения статистики
    """
    total_books = Book.objects.count()
    total_authors = Person.objects.filter(authored_books__isnull=False).distinct().count()
    total_downloads = Book.objects.filter(
        download_count__isnull=False
    ).aggregate(
        total=Count('download_count')
    )['total'] or 0

    return Response({
        'total_books': total_books,
        'total_authors': total_authors,
        'total_downloads': total_downloads
    })