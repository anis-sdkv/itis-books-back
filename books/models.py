from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User

class Author(models.Model):
    name = models.CharField(max_length=255, unique=True)
    bio = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='author_profile'
    )

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
        ('archived', 'В архиве'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    publication_year = models.IntegerField(
        blank=True, 
        null=True,
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(2100)
        ]
    )
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    file = models.FileField(upload_to='book_files/', blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True, null=True, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    authors = models.ManyToManyField(Author, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')
    
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='created_books'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

class Favorite(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='favorites'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='favorited_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-created_at']

class Comment(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='comments'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

class Quote(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='quotes'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='quotes'
    )
    text = models.TextField()
    page_number = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

class Rating(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    book = models.ForeignKey(
        Book, 
        on_delete=models.CASCADE, 
        related_name='ratings'
    )
    value = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book') 