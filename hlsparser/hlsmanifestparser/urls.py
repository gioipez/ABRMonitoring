from django.urls import path
from hlsmanifestparser.views import hls_manifest_parser

urlpatterns = [
    path('hlsmanifest/', hls_manifest_parser, name="hls-manifest-parser")
]
