from rest_framework import serializers
from api.models import (
        Collection,
        Document,
        Page,
        Sentence,
        Location,)


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Collection
        fields = ('url', 'text', 'documents',)


class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Document
        fields = ('url', 'title', 'pubdate', 'author', 'external_url',
                'collection', 'pages',)


class PageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Page
        fields = ('url', 'document', 'sentences',)


class SentenceSerializer(serializers.HyperlinkedModelSerializer):
    document = serializers.HyperlinkedRelatedField(read_only=True,
                        view_name='document-detail', source='page.document')

    class Meta:
        model = Sentence
        fields = ('url', 'text', 'i_score', 'document',)


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('url', 'text', 'geom', 'poly', 'ptype', )
