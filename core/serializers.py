from django.conf import settings
from django.urls import reverse
from rest_framework import serializers

from core.models import Upload


class UploadSerializer(serializers.Serializer):
    # The default=None approach is slightly hacky, but it works here...
    file = serializers.FileField(default=None)
    url = serializers.URLField(allow_blank=True, default=None)

    def validate(self, data):
        if not any(data.values()):  # not any() = none of X are true-ish
            raise serializers.ValidationError("Neither `file` nor `url` specified.")

        if all(data.values()):
            raise serializers.ValidationError(
                "Both `file` and `url` specified. Pick one and try again."
            )

        return data


class UploadSuccessSerializer(serializers.ModelSerializer):
    upload_url = serializers.SerializerMethodField("get_upload_url")

    def get_upload_url(self, obj):
        base_url = settings.BASE_APP_URL.strip("/")
        access_path = reverse("upload-access", args=[obj.id])
        return f"{settings.BASE_APP_URL}{access_path}"

    class Meta:
        model = Upload
        fields = ["password", "id", "upload_url"]


class SummarySerializer(serializers.Serializer):
    def to_representation(self, queryset):
        print(queryset)
        from operator import itemgetter
        from itertools import groupby

        key = itemgetter("created_at__date")
        iter = groupby(sorted(queryset.all(), key=key), key=key)

        serialized = {}
        for date, uploads in iter:
            serialized[str(date)] = {}  # Could have been a DefaultDict as well.
            for upload in uploads:
                serialized[str(date)][str(upload["id"])] = upload["successful_attempts"]

        print(serialized)
        return serialized
