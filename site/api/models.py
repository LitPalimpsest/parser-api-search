from django.db import models


class Collection(models.Model):
    text = models.CharField(max_length=64, null=False)

    def __unicode__(self):
        return self.text


class Document(models.Model):
    docid = models.CharField(max_length=96, null=False)
    title = models.TextField(null=False)
    url = models.CharField(max_length=128, null=True)
    pubdate = models.DateField(null=True)
    type = models.CharField(max_length=32, null=True)
    author = models.TextField(null=True)
    majlang = models.CharField(max_length=3, null=True)
    collection = models.ForeignKey(Collection, null=False, default=0)

    def __unicode__(self):
        return self.title
