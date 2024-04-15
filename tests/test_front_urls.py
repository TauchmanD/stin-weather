from django.test import SimpleTestCase
from django.urls import reverse, resolve
from front.views import index


class TestFrontUrls(SimpleTestCase):
    def test_index_url(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func, index)
