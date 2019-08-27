from core.models import Upload
from django import forms


class UploadForm(forms.ModelForm):

    CHOICES = [("file_upload", "File"), ("url_upload", "URL")]

    # For better access later on.
    CHOICES_IDS = [choice[0] for choice in CHOICES]

    upload_type = forms.ChoiceField(
        choices=CHOICES, widget=forms.RadioSelect, initial="file_upload"
    )

    class Meta:
        model = Upload
        fields = ["upload_type", "url", "file"]

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")
        url = cleaned_data.get("url")
        upload_type = cleaned_data.get("upload_type")

        if upload_type not in self.CHOICES_IDS:
            raise forms.ValidationError("Unknown upload type value.")

        if upload_type == "file_upload" and not file:
            raise forms.ValidationError("File upload selected, but no file sent.")

        if upload_type == "url_upload" and not url:
            raise forms.ValidationError("URL upload selected, but no URL sent.")


class PasswordForm(forms.ModelForm):
    class Meta:
        model = Upload
        fields = ["password"]
        widgets = {"password": forms.PasswordInput}

    def clean(self):
        cleaned_data = super(PasswordForm, self).clean()
        password = cleaned_data.get("password")

        if not password == self.instance.password:
            self.add_error("password", "Password does not match.")
