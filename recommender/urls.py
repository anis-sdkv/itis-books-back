from django.urls import path

from recommender.views import RecommendBooksView

urlpatterns = [
    path('recommend/', RecommendBooksView.as_view()),
]
