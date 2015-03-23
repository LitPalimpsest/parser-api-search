from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,)
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from rest_framework import viewsets
import re
import string
from api.forms import SearchForm
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
    docs = decs_list = colls_list = errors = text = decade = collection = None
    collection_name = ""

    form = SearchForm(request.GET)
    if form.is_valid():
        params = {}
        text = form.cleaned_data['text']
        pattern = re.compile('[^a-zA-Z0-9 ]+')
        if text:
            text = string.replace(pattern.sub('', text).strip(), ' ', '&')
            text_filter = ""
            if text != '*':
                params['query_string'] = '{0}:*'.format(text)
                text_filter = "AND t.fts_tokens @@ to_tsquery(%(query_string)s)"
            text = string.replace(text, '&', ' ')

        collection = request.GET.get('collection', None)
        coll_filter = ""
        if collection:
            c = Collection.objects.get(id=collection)
            collection_name = c.text
            collection = int(collection)
            params['coll_id'] = collection
            coll_filter = "AND c.id = %(coll_id)s"

        decade = request.GET.get('decade', None)
        dec_filter = ""
        if decade:
            dec_filter = "AND (EXTRACT(DECADE FROM d.pubdate)||'0')"
            if decade == "NA":
                dec_filter = "{0} IS NULL".format(dec_filter)
            else:
                params['dec_id'] = decade
                dec_filter = "{0} = %(dec_id)s".format(dec_filter)

        cursor = connection.cursor()
        colls_sql = """
            SELECT
                c.id,
                c.text,
                COUNT(*) AS hits
            FROM sentence_fts AS t
            JOIN api_sentence AS s ON t.sentence_id = s.id
            JOIN api_page AS p ON s.page_id = p.id
            JOIN api_document AS d ON p.document_id = d.id
            JOIN api_collection AS c ON d.collection_id = c.id  {0} {1} {2}
            GROUP BY c.id, c.text
            ORDER BY c.text""".format(text_filter, dec_filter, coll_filter)
        cursor.execute(colls_sql, params)
        cols = ['id', 'collection', 'hits']
        colls_list = [dict(zip(cols, row)) for row in cursor.fetchall()]

        decs_sql = """
            SELECT
                CASE
                    WHEN d.pubdate IS NULL THEN 'NA'
                    ELSE EXTRACT(DECADE FROM d.pubdate)||'0'
                END AS decade,
                COUNT(*) AS hits
            FROM sentence_fts AS t
            JOIN api_sentence AS s ON t.sentence_id = s.id
            JOIN api_page AS p ON s.page_id = p.id
            JOIN api_document AS d ON p.document_id = d.id
            JOIN api_collection AS c ON d.collection_id = c.id {0} {1} {2}
            GROUP BY decade
            ORDER BY decade""".format(text_filter, dec_filter, coll_filter)
        cursor.execute(decs_sql, params)
        cols = ['decade', 'hits']
        decs_list = [dict(zip(cols, row)) for row in cursor.fetchall()]

        docs_sql = """
            SELECT
                d.id,
                d.title,
                COUNT (d.id) AS hits
            FROM sentence_fts AS t
            JOIN api_sentence AS s ON t.sentence_id = s.id
            JOIN api_page AS p ON s.page_id = p.id
            JOIN api_document AS d ON p.document_id = d.id
            JOIN api_collection AS c ON d.collection_id = c.id {0} {1} {2}
            GROUP BY d.id
            ORDER BY hits DESC""".format(text_filter, dec_filter, coll_filter)
        cursor.execute(docs_sql, params)
        cols = ['id', 'title', 'hits']
        docs_list = [dict(zip(cols, row)) for row in cursor.fetchall()]
        docs = get_paginated_results(request, docs_list)
    else:
        errors = form.errors
    return render(request, 'search_results.html', {
        'form': form,
        'colls': colls_list,
        'decs': decs_list,
        'docs': docs,
        'errors': errors,
        'text': text,
        'decade': decade,
        'collection': collection,
        'collection_name': collection_name})


def document(request, document_id):
    # Get document
    doc = Document.objects.get(pk=document_id)
    #log.debug('Document: %s-%s' % (doc.id, doc.url))

    # Get snippets containing text
    params = {'document_id': document_id}
    text = request.GET.get('text', None)
    pattern = re.compile('[^a-zA-Z0-9 ]+')
    if text:
        text = string.replace(pattern.sub('', text).strip(), ' ', '&')
        text_filter = ""
        if text != '*':
            params['query_string'] = '{0}:*'.format(text)
            text_filter = "AND t.fts_tokens @@ to_tsquery(%(query_string)s)"
        text = string.replace(text, '&', ' ')
    sql = """
        SELECT
            s.text AS snippet,
            p.url AS page_url
        FROM sentence_fts AS t
        JOIN api_sentence AS s ON t.sentence_id = s.id
        JOIN api_page AS p ON s.page_id = p.id
        JOIN api_document AS d ON p.document_id = d.id {0}
        AND d.id = %(document_id)s
        """.format(text_filter)
    cursor = connection.cursor()
    cursor.execute(sql, params)
    cols = ['snippet', 'url']
    snippet_list = [dict(zip(cols, row)) for row in cursor.fetchall()]

    # Convert XML character references to HTML entities
    # for sentence in sentence_list:
    #     sentence['text'] = unicode(escape(sentence['text']).encode(
    #         'ascii', 'xmlcharrefreplace'))
    #     sentence['sentence'] = unicode(escape(sentence['sentence']).encode(
    #         'ascii', 'xmlcharrefreplace'))
    snippets = get_paginated_results(request, snippet_list, num_records=10)

    return render(request, 'document.html', {
        'doc': doc,
        'text': text,
        'snippets': snippets, })


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
