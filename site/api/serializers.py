from rest_framework import serializers
from api.models import Collection, Document


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    documents = serializers.HyperlinkedRelatedField(many=True, read_only=True,
            view_name='document-detail')

    class Meta:
        model = Collection
        fields = ('url', 'text', 'documents',)


class DocumentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Document
        fields = ('url', 'title', 'pubdate', 'author', 'external_url', 'collection',)
