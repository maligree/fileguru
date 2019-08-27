from core.api_views import AccessAPIView, SummaryAPIView, UploadAPIView
from core.views import IndexView, PasswordView, SummaryView, UploadView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

api_patterns = [
    # path('api-auth/', include('rest_framework.urls')),
    path("upload/", UploadAPIView.as_view(), name="api-upload"),
    path("access/<uuid:pk>/", AccessAPIView.as_view(), name="api-access"),
    path("summary/", SummaryAPIView.as_view(), name="api-summary"),
]

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("upload/", UploadView.as_view(), name="upload-form"),
    path("access/<uuid:pk>/", PasswordView.as_view(), name="upload-access"),
    path("summary/", SummaryView.as_view(), name="upload-summary"),
    # Use built-in auth for handling logins and logouts.
    path("login/", LoginView.as_view(template_name="core/login.html"), name="login"),
    path(
        "logout/", LogoutView.as_view(template_name="core/logout.html"), name="logout"
    ),
    # Nest all API-related patterns under /api
    path("api/", include(api_patterns)),
]
