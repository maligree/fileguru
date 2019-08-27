import string
from datetime import datetime, timedelta
from random import choices
from uuid import uuid4

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


def generate_upload_password():
    return "".join(
        choices(
            string.ascii_uppercase + string.digits, k=settings.UPLOAD_PASSWORD_LENGTH
        )
    )


def generate_expiry_datetime():
    return datetime.now() + timedelta(hours=settings.UPLOAD_EXPIRY_HOURS)


class Upload(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    # 32 seems sane (if adjusted from admin panel),
    # but auto-generated password is shorter than that.
    password = models.CharField(max_length=32, default=generate_upload_password)

    file = models.FileField(upload_to="uploads/", blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    successful_attempts = models.IntegerField(default=0)
    failed_attempts = models.IntegerField(default=0)

    expires_at = models.DateTimeField(default=generate_expiry_datetime)
    created_at = models.DateTimeField(auto_now_add=True)


class UserAgent(models.Model):
    user = models.OneToOneField(User, models.CASCADE, related_name="last_user_agent")

    # The UA string can get pretty long and this is not a table where performance paramount.
    # See https://stackoverflow.com/a/13210391/320475 for extra context and a really
    # good long-term solution that includes a hashed binary field for quick comparisons.
    value = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
