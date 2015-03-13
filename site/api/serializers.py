from rest_framework import serializers
from api.models import Collection


class CollectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Collection
        fields = ('text', 'url',)
