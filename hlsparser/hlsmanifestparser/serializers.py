from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from hlsmanifestparser.models import HLSManifestParser

class HLSPManifestParserSerializer(ModelSerializer):
    asset_name = serializers.CharField(required=True, allow_blank=False, max_length=300)
    base_url = serializers.CharField(required=True, allow_blank=False, max_length=300)

    class Meta:
       model = HLSManifestParser
       fields = ["asset_name", "base_url"]
