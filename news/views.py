from django.shortcuts import render
from django.views.generic import ListView

from news.models import News

# Create your views here.
class HomePageViews(ListView):
    template_name = "index.html"
    model = News

    def get_context_data(self, **kwargs) -> str:
        context = super().get_context_data(**kwargs)
        context["news"] = News.objects.filter().order_by("-pubdate")[:5]
        return context