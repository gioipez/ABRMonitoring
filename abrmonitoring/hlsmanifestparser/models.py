from django.db import models

class HLSManifestParser(models.Model):
    asset_name = models.CharField(max_length=300)
    base_url = models.CharField(max_length=300)

