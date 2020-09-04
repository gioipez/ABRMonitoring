from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from hlsmanifestparser.models import HLSManifestParser

class HLSPManifestParserSerializer(ModelSerializer):
    manifest_url = serializers.CharField(required=True, allow_blank=False, max_length=300)

    class Meta:
       model = HLSManifestParser
       fields = ["manifest_url"]
