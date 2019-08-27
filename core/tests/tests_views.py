from core.models import Upload
from django.conf import settings
from django.contrib.auth.models import User
from django.http.response import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse
from freezegun import freeze_time


def create_url_upload(url):
    upload = Upload()
    upload.url = url
    upload.save()
    return upload


def create_file_upload(url):
    # TODO
    upload = Upload()
    upload.url = url
    upload.save()
    return upload


class UploadViewTests(TestCase):
    def setUp(self):
        user = User.objects.create_user("testuser", "testuser@example.com", "testuser")
        self.test_user = user

    def test_login_required(self):
        """
        Unauthenticated users are redirected to the login screen.
        """

        response = self.client.get(reverse("upload-form"))

        # See if a temporary redirect happens...
        self.assertEqual(response.status_code, 302)

        # Slightly redundant, but could alert early about unexpected changes/issues.
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertTrue(response.has_header("Location"))

        # Quick check, totally ignorant of the ?next= parameter.
        self.assertTrue(response.get("Location").startswith(settings.LOGIN_URL))

    def test_access_is_password_protected(self):
        """
        Trivial test to make sure a passsword form is presented.
        """

        # Directly create an Upload object in the DB.
        upload = create_url_upload("https://google.com/robots.txt")
        response = self.client.get(reverse("upload-access", args=[upload.id]))

        # Ensure request does not error, no special code expected here.
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Password")

    def test_upload_creates_db_entry_properly(self):
        """
        Submit a form to the /upload endpoint and check if DB is properly populated.
        """

        self.client.force_login(self.test_user)
        response = self.client.post(
            reverse("upload-form"), {"url": "https://fb.com/robots.txt"}
        )
        upload_obj = response.context["upload"]

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Password")

        # Ensure rendered form contains the generated password.
        self.assertContains(response, upload_obj.password)

    def test_password_unlocks_access_redirect(self):
        """

        Will also test if access counter is properly incremented.
        """
        test_url = "https://github.com/robots.txt"
        upload_obj = create_url_upload(test_url)

        self.assertEqual(upload_obj.successful_attempts, 0)

        response = self.client.post(
            reverse("upload-access", args=[upload_obj.id]),
            {"password": upload_obj.password},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.has_header("Location"))
        self.assertEqual(response.get("Location"), test_url)

        upload_obj.refresh_from_db()
        self.assertEqual(upload_obj.successful_attempts, 1)

    def test_404_after_expired(self):
        test_url = "https://github.com/robots.txt"

        # Freezing creation, since this would not work during request, as comaprison is done inside DB.
        # This is slightly contrived for this case, but I like freezegun.
        with freeze_time("2000-01-01"):
            upload_obj = create_url_upload(test_url)

        response = self.client.get(reverse("upload-access", args=[upload_obj.id]))
        self.assertEqual(response.status_code, 404)
