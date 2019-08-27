from core.models import Upload


# Just for fun, to keep in line with Django's way of handling View extensions.
# A helper function would do just as well.
class UploadSummaryMixin:
    def get_summary(self):
        entries = (
            Upload.objects.values("id", "successful_attempts", "created_at__date")
            .filter(successful_attempts__gt=0)
            .order_by("-created_at")
        )
        return entries
