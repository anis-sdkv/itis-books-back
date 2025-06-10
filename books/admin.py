from django.contrib import admin
from .models import *

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)
    list_filter = ('user',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class AuthorInline(admin.TabularInline):
    model = Book.authors.through
    extra = 1

class GenreInline(admin.TabularInline):
    model = Book.genres.through
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_year', 'status')
    search_fields = ('title', 'isbn')
    list_filter = ('status', 'genres', 'authors')
    exclude = ('authors', 'genres')
    inlines = [AuthorInline, GenreInline]

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at')
    list_filter = ('created_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'is_approved')
    list_filter = ('is_approved', 'created_at')

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'is_public')
    list_filter = ('is_public', 'created_at')

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'value')
    list_filter = ('value',) 