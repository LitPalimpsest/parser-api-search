from rest_framework import viewsets
from api.models import Collection
from api.serializers import CollectionSerializer


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Collections to be viewed
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
