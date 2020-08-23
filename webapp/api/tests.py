from django.urls import reverse
from rest_framework.test import APITestCase


class HealthApiTest(APITestCase):

    def test_get_health_record(self):
        self.client.get(reverse('get-health-record'))