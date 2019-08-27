import os
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.common import UploadSummaryMixin
from core.models import Upload
from core.permissions import HasProperPassphrase
from core.serializers import (
    SummarySerializer,
    UploadSerializer,
    UploadSuccessSerializer,
)


class UploadAPIView(APIView):
    """
    Handles creating new Upload entries in the DB.

    This endpoints accepts either an application/json request with a JSON body and a URL key,
    or a file with the appropriate content-type set.

    Return 201 on successful creation or 400 for validation errors.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # FileUploadParser accepts all MIME types, so it needs
    # to be second to give JSONParser a chance.
    parser_classes = (JSONParser, FileUploadParser)

    def put(self, request):

        serializer = UploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Bail out early

        if serializer.validated_data["file"] is not None:
            file_obj = serializer.validated_data["file"]
            upload = Upload()
            upload.file = file_obj
            upload.save()
        else:
            upload = Upload()
            upload.url = serializer.data["url"]
            upload.save()

        serializer = UploadSuccessSerializer(upload)
        return Response(serializer.data, status=201)


class AccessAPIView(APIView):
    """
    Asks for a password and serves the file or redirects to the given URL.
    """

    permission_classes = [HasProperPassphrase]

    def get(self, request, pk):
        obj = get_object_or_404(Upload, pk=pk, expires_at__gt=datetime.now())
        self.check_object_permissions(request, obj)

        # Increment attempt counter.
        form.instance.successful_attempts = F("successful_attempts") + 1

        if obj.file:
            file_path = obj.file.path
            with open(file_path, "rb") as f_out:
                response = HttpResponse(f_out.read())
                response[
                    "Content-Disposition"
                ] = "attachment; filename=" + os.path.basename(file_path)
            return response
        else:
            return Response({"url": obj.url})


class SummaryAPIView(APIView, UploadSummaryMixin):
    """
    Displays some statistics on the submitted uploads. 
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entries = self.get_summary()
        serializer = SummarySerializer(entries)
        return Response(serializer.data)
