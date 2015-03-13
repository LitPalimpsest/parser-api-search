from rest_framework import serializers
from api.models import Collection, Document


class CollectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Collection
        fields = ('text', 'url',)


class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Document
        fields = ('title', 'pubdate', 'author', 'external_url', 'collection', 'url',)
