from rest_framework import viewsets
from api.models import Collection, Document, Page, Sentence
from api.serializers import (
        CollectionSerializer,
        DocumentSerializer,
        PageSerializer,
        SentenceSerializer,)


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


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Pages to be viewed
    """
    queryset = Page.objects.all()
    serializer_class = PageSerializer


class SentenceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Sentences to be viewed
    """
    queryset = Sentence.objects.all()
    serializer_class = SentenceSerializer
