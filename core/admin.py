from django.contrib import admin

from .models import Upload, UserAgent


@admin.register(Upload)
class UploadAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "url",
        "file",
        "successful_attempts",
        "failed_attempts",
        "created_at",
        "expires_at",
    ]

    readonly_fields = ["id", "successful_attempts", "failed_attempts"]


@admin.register(UserAgent)
class UserAgentAdmin(admin.ModelAdmin):
    list_display = ["user", "value", "updated_at"]
    search_fields = ["user"]
