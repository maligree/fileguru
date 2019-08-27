from django.urls import reverse
from rest_framework.test import APITestCase


class UploadTests(APITestCase):
    def test_auth_required(self):
        # Empty request, this is just a smoke test.
        response = self.client.post(reverse("api-upload"), {}, format="json")

        # We expect to be rejected.
        self.assertEqual(response.status_code, 401)
