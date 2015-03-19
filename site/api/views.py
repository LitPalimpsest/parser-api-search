from api.forms import SearchForm

from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,)
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets
from api.models import (
        Collection,
        Document,
        Page,
        Sentence,
        Location,)
from api.serializers import (
        CollectionSerializer,
        DocumentSerializer,
        PageSerializer,
        SentenceSerializer,
        LocationSerializer,)


def home(request):
    return HttpResponseRedirect('/search/')


def search(request):
    results = errors = text = None
    form = SearchForm(request.GET)
    if form.is_valid():
        cursor = connection.cursor()
        text = form.cleaned_data['text']
        params = {'query_string': '{0}:*'.format(text)}
        where_clause = ""
        if text != '*':
            where_clause = "WHERE t.fts_tokens @@ to_tsquery(%(query_string)s)"
        sql = """
            SELECT
                d.id,
                d.title,
                COUNT (d.id) AS hits
            FROM
                sentence_fts AS t
            JOIN api_sentence AS s ON t.sentence_id = s.id
            JOIN api_page AS p ON s.page_id = p.id
            JOIN api_document AS d ON p.document_id = d.id {0}
            GROUP BY d.id
            ORDER BY hits DESC""".format(where_clause)
        cursor.execute(sql, params)
        cols = ['id', 'document', 'hits']
        results_list = [dict(zip(cols, row)) for row in cursor.fetchall()]
        results = get_paginated_results(request, results_list)
    else:
        errors = form.errors
    return render(request, 'search_results.html', {
        'form': form,
        'results': results,
        'errors': errors,
        'text': text, })


def get_paginated_results(request, model_list, num_records=25):
    paginator = Paginator(model_list, num_records)
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        results = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        results = paginator.page(paginator.num_pages)
    return results


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


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows Locations to be viewed
    """
    queryset = Location.objects.filter(point__isnull=False)
    serializer_class = LocationSerializer
