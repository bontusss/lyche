from django.test import TestCase

from news.models import News
from django.utils import timezone
from django.urls.base import reverse

# Create your tests here.
class NewsTests(TestCase):
    def setUp(self):
        self.news = News.objects.create(
            title = "Title sample",
            description = "Sample description",
            pubdate = timezone.now(),
            link = "https://samplelink.com",
            image = "https://sample.com",
            source = "CNN",
            guid = "https://guid.com"
        )

    def test_news_content(self):
        self.assertEqual(self.news.description, "Sample description")
        self.assertEqual(self.news.title, "Title sample")
        self.assertEqual(self.news.link, "https://samplelink.com")
        self.assertEqual(self.news.source, "CNN")


    def test_news_str_representation(self):
        self.assertEqual(str(self.news), "CNN: Title sample")


    def test_homepage_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_home_page_uses_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response, "index.html")