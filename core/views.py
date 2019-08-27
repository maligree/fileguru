import os
from datetime import datetime

from core.common import UploadSummaryMixin
from core.forms import PasswordForm, UploadForm
from core.models import Upload
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView


class IndexView(TemplateView):
    template_name = "core/index.html"


class UploadView(LoginRequiredMixin, CreateView):
    template_name = "core/upload.html"
    # model = Upload
    form_class = UploadForm
    # fields = ["file", "url"]

    def form_valid(self, form):
        form.save()
        return render(self.request, "core/success.html", {"upload": form.instance})


class PasswordView(UpdateView):
    model = Upload
    form_class = PasswordForm
    queryset = Upload.objects.filter(expires_at__gte=datetime.now())
    template_name = "core/password.html"

    def form_valid(self, form):

        # Increment access counter...
        form.instance.successful_attempts = F("successful_attempts") + 1
        form.instance.save()

        if form.instance.file:
            # Serve the file directly.
            file_path = form.instance.file.path
            with open(file_path, "rb") as f_out:
                response = HttpResponse(f_out.read())
                response[
                    "Content-Disposition"
                ] = "attachment; filename=" + os.path.basename(file_path)
                return response
        else:
            # Hand the user off to the originally submitted URL.
            return redirect(form.instance.url)

    def form_invalid(self, form):
        # TODO failed access counter here
        return super().form_invalid(form)


class SummaryView(View, UploadSummaryMixin):
    def get(self, request):
        # We'll pass them straight to the template where regroup() will handle the rest.
        entries = self.get_summary()
        return render(request, "core/summary.html", {"entries": entries})
