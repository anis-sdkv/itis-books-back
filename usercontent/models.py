from django.db import models
from django.conf import settings

class LikedBook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_books')
    gutenberg_id = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'gutenberg_id')
        ordering = ['-added_at']

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    gutenberg_id = models.IntegerField()
    rating = models.PositiveSmallIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Quote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quotes')
    gutenberg_id = models.IntegerField()
    text = models.TextField()
    page_reference = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
