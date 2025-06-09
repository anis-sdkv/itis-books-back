from django.urls import path
from .views import RegisterView, UserListView, UserDetailView, ProfileView, LoginView, RefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshView.as_view(), name='token_refresh'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
