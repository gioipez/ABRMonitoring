from django.db import models

class HLSManifestParser(models.Model):
    manifest_url = models.CharField(max_length=300)

