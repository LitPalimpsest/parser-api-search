from django.db import models


class Collection(models.Model):
    text = models.CharField(max_length=64, null=False)

    def __unicode__(self):
        return self.text
