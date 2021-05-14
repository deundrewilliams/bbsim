from django.db import models


class Contestant(models.Model):

    name = models.TextField(blank=False, null=False)
