from django.contrib.gis.db import models


class Collection(models.Model):
    text = models.CharField(max_length=64, null=False)

    def __unicode__(self):
        return self.text


class Document(models.Model):
    docid = models.CharField(max_length=96, null=False)
    title = models.TextField(null=False)
    external_url = models.CharField(max_length=128, null=True, db_column='url')
    pubdate = models.DateField(null=True)
    type = models.CharField(max_length=32, null=True)
    author = models.TextField(null=True)
    majlang = models.CharField(max_length=3, null=True)
    collection = models.ForeignKey(Collection, null=False, default=0)

    def __unicode__(self):
        return self.title


class Page(models.Model):
    identifier = models.URLField(null=True, db_column='url')
    lang = models.CharField(max_length=16, null=True)
    document = models.ForeignKey(Document, null=False)

    def __unicode__(self):
        return self.url


class Sentence(models.Model):
    identifier = models.CharField(max_length=10, null=False)
    text = models.TextField(null=False)
    xml = models.TextField(null=False)
    page = models.ForeignKey(Page, null=False, default=0)
    i_score = models.FloatField(null=True)
    palsnippet = models.BooleanField(null=False, default=False)

    def __unicode__(self):
        return self.text


class Location(models.Model):
    text = models.CharField(max_length=128, null=False)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    geom = models.PointField(null=True, srid=4326)
    poly = models.PolygonField(null=True, srid=4326)
    ptype = models.CharField(max_length=32, null=True)
    in_country = models.CharField(max_length=2, null=True)
    gazref = models.CharField(max_length=32, null=True)
    feature_type = models.CharField(max_length=32, null=True)
    pop_size = models.BigIntegerField(null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.text


class LocationMention(models.Model):
    text = models.CharField(max_length=128, null=False)
    start_word = models.CharField(max_length=10, null=False)
    end_word = models.CharField(max_length=10, null=False)
    document = models.ForeignKey(Document, null=False, default=0)
    page = models.ForeignKey(Page, null=False, default=0)
    sentence = models.ForeignKey(Sentence, null=False, default=0)
    location = models.ForeignKey(Location, null=False, default=0)

    def __unicode__(self):
        return self.text


class PartOfSpeech(models.Model):
    tag = models.CharField(max_length=4, null=False)
    description = models.CharField(max_length=40, null=True)

    def __unicode__(self):
        return self.description


class POSMention(models.Model):
    text = models.CharField(max_length=128, null=False)
    pos = models.ForeignKey(PartOfSpeech, null=False, default=0)
    sentence = models.ForeignKey(Sentence, null=False, default=0)

    def __unicode__(self):
        return self.text
