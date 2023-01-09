from django.urls import path

from news.views import HomePageViews

urlpatterns = [
    path("", HomePageViews.as_view(), name="homepage")
]