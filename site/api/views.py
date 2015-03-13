from rest_framework import viewsets
from api.models import Collection, Document
from api.serializers import CollectionSerializer, DocumentSerializer


class CollectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Collections to be viewed
    """
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


class DocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Documents to be viewed
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
