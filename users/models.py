from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    ROLES = (
        ('reader', 'Читатель'),
        ('writer', 'Писатель'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор'),
    )
    
    role = models.CharField(max_length=20, choices=ROLES, default='reader')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    
    # Переопределяем поля из AbstractUser с related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_writer(self):
        return self.role == 'writer'
    
    @property
    def is_admin(self):
        return self.role in ['admin', 'moderator']

class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'following_user')
        ordering = ['-created_at']
