from django.test import TestCase
from news.subscribers import send_new_week_categories


# Create your tests here.


class SubscribersTestCase(TestCase):
    def test(self):
        send_new_week_categories()
