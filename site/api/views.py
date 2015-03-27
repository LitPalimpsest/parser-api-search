from django.core.paginator import (
    Paginator,
    EmptyPage,
    PageNotAnInteger,)
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
import logging
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
        ListDocumentSerializer,
        RetrieveDocumentSerializer,
        PageSerializer,
        SentenceSerializer,
        LocationSerializer,)

log = logging.getLogger(__name__)

def home(request):
    return HttpResponseRedirect('/search/')


def search(request):
    docs = decs_list = colls_list = locs_list = errors = None
    text = locid = location = decade = collection = None
    location_name = collection_name = ""

    form = SearchForm(request.GET)
    if form.is_valid():
        params = {}
        text = form.cleaned_data['text']
        log.debug('Search term: %s' % text)
        pattern = re.compile('[^a-zA-Z0-9\* ]+')
        if text:
            text = pattern.sub('', text).strip()
            text_filter = ""
            if text != '*':
                query_string = ""
                for term in text.split():
                    query_string += '{0}:* & '.format(term)
                query_string = query_string[:-3]
                params['query_string'] = query_string
                text_filter = "AND t.fts_tokens @@ to_tsquery(%(query_string)s)"
            text = ' '.join(text.split())

        location = request.GET.get('loc', None)
        loc_filter = ""
        if location:
            l = Location.objects.get(id=location)
            location_name = l.text
            location = int(location)
            params['loc_id'] = location
            loc_filter = "AND l.id = %(loc_id)s"

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
        locs_sql = """
            SELECT
                l.id AS locid,
                l.text AS location,
                ST_AsText(l.geom) AS point,
                ST_AsText(l.poly) AS poly,
                COUNT(*) AS hits
            FROM
                (SELECT
                    DISTINCT ON(s.text) s.text,
                    s.id,
                    s.page_id
                FROM sentence_fts AS t
                JOIN api_sentence AS s ON t.sentence_id = s.id
                {0}) AS snips
            JOIN api_locationmention AS m ON snips.id = m.sentence_id
            JOIN api_location AS l ON m.location_id = l.id
            JOIN api_page AS p ON snips.page_id = p.id
            JOIN api_document AS d ON p.document_id = d.id
            JOIN api_collection AS c ON d.collection_id = c.id {1} {2} {3}
            GROUP BY locid, location, point, poly
            """.format(text_filter, dec_filter, coll_filter, loc_filter)
        cursor.execute(locs_sql, params)
        locs = ['id', 'location', 'point', 'poly', 'hits']
        locs_list = [dict(zip(locs, row)) for row in cursor.fetchall()]

        colls_sql = """
            SELECT
                c.id,
                c.text,
                COUNT(*) AS hits
            FROM
                (SELECT
                    DISTINCT ON(s.text) s.text,
                    s.id,
                    s.page_id
                FROM sentence_fts AS t
                JOIN api_sentence AS s ON t.sentence_id = s.id
                {0}) AS snips
            JOIN api_locationmention AS m ON snips.id = m.sentence_id
            JOIN api_location AS l ON m.location_id = l.id
            JOIN api_page AS p ON snips.page_id = p.id
            JOIN api_document AS d ON p.document_id = d.id
            JOIN api_collection AS c ON d.collection_id = c.id {1} {2} {3}
            GROUP BY c.id, c.text
            ORDER BY c.text
            """.format(text_filter, dec_filter, coll_filter, loc_filter)
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
            FROM
                (SELECT
                    DISTINCT ON(s.text) s.text,
                    s.id,
                    s.page_id
                FROM sentence_fts AS t
                JOIN api_sentence AS s ON t.sentence_id = s.id
                {0}) AS snips
            JOIN api_locationmention AS m ON snips.id = m.sentence_id
            JOIN api_location AS l ON m.location_id = l.id
            JOIN api_page AS p ON snips.page_id = p.id
            JOIN api_document AS d ON p.document_id = d.id
            JOIN api_collection AS c ON d.collection_id = c.id {1} {2} {3}
            GROUP BY decade
            ORDER BY decade
            """.format(text_filter, dec_filter, coll_filter, loc_filter)
        cursor.execute(decs_sql, params)
        cols = ['decade', 'hits']
        decs_list = [dict(zip(cols, row)) for row in cursor.fetchall()]

        docs_sql = """
            SELECT
                d.id,
                d.title,
                COUNT (d.id) AS hits
            FROM
                (SELECT
                    DISTINCT ON(s.text) s.text,
                    s.id,
                    s.page_id
                FROM sentence_fts AS t
                JOIN api_sentence AS s ON t.sentence_id = s.id
                {0}) AS snips
            JOIN api_locationmention AS m ON snips.id = m.sentence_id
            JOIN api_location AS l ON m.location_id = l.id
            JOIN api_page AS p ON snips.page_id = p.id
            JOIN api_document AS d ON p.document_id = d.id
            JOIN api_collection AS c ON d.collection_id = c.id {1} {2} {3}
            GROUP BY d.id
            ORDER BY hits DESC
            """.format(text_filter, dec_filter, coll_filter, loc_filter)
        cursor.execute(docs_sql, params)
        cols = ['id', 'title', 'hits']
        docs_list = [dict(zip(cols, row)) for row in cursor.fetchall()]
        docs = get_paginated_results(request, docs_list)
    else:
        errors = form.errors
    return render(request, 'search_results.html', {
        'form': form,
        'locs': locs_list,
        'colls': colls_list,
        'decs': decs_list,
        'docs': docs,
        'errors': errors,
        'text': text,
        'decade': decade,
        'collection': collection,
        'locid': location,
        'location': location_name,
        'collection_name': collection_name})


def document(request, document_id):
    # Get document
    doc = Document.objects.get(pk=document_id)
    log.debug('Document: %s-%s' % (doc.id, doc.docid))

    # Get snippets containing text
    params = {'document_id': document_id}
    text = request.GET.get('text', None)
    pattern = re.compile('[^a-zA-Z0-9\* ]+')
    if text:
        text = pattern.sub('', text).strip()
        text_filter = ""
        if text != '*':
            query_string = ""
            for term in text.split():
                query_string += '{0}:* & '.format(term)
            query_string = query_string[:-3]
            params['query_string'] = query_string
            text_filter = "AND t.fts_tokens @@ to_tsquery(%(query_string)s)"
        text = ' '.join(text.split())
    location = request.GET.get('loc', None)
    loc_filter = ""
    if location:
        location = int(location)
        params['loc_id'] = location
        loc_filter = "AND l.id = %(loc_id)s"
    sql = """
        SELECT
            snips.text AS snippet,
            p.url AS page_url
        FROM
            (SELECT
                DISTINCT ON(s.text) s.text,
                s.id,
                s.page_id,
                s.i_score
            FROM sentence_fts AS t
            JOIN api_sentence AS s ON t.sentence_id = s.id {0}) AS snips
        JOIN api_locationmention AS m ON snips.id = m.sentence_id
        JOIN api_location AS l ON m.location_id = l.id
        JOIN api_page AS p ON snips.page_id = p.id
        JOIN api_document AS d ON p.document_id = d.id
        AND d.id = %(document_id)s {1}
        ORDER BY snips.i_score DESC
        """.format(text_filter, loc_filter)
    cursor = connection.cursor()
    cursor.execute(sql, params)
    cols = ['snippet', 'url']
    snippet_list = [dict(zip(cols, row)) for row in cursor.fetchall()]
    snippets = get_paginated_results(request, snippet_list, num_records=10)

    locs_sql = """
        SELECT
            DISTINCT ON(text) m.text,
            l.id
        FROM sentence_fts AS t
        JOIN api_sentence AS s ON s.id = t.sentence_id
        JOIN api_page AS p ON p.id = s.page_id
        JOIN api_document AS d ON d.id = p.document_id
        JOIN api_locationmention AS m ON m.sentence_id = s.id
        JOIN api_location AS l ON l.id = m.location_id {0}
        AND d.id = %(document_id)s
        ORDER BY m.text DESC""".format(text_filter)
    cursor = connection.cursor()
    cursor.execute(locs_sql, params)
    cols = ['location', 'locid']
    locs_list = [dict(zip(cols, row)) for row in cursor.fetchall()]

    return render(request, 'document.html', {
        'doc': doc,
        'text': text,
        'snippets': snippets,
        'locs': locs_list})


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


class MultiSerializerViewSet(viewsets.ReadOnlyModelViewSet):
    def get_serializer_class(self):
            return self.serializers.get(self.action,
                        self.serializers['list'])


class DocumentViewSet(MultiSerializerViewSet):
    """
    API endpoint that allows Documents to be viewed
    """

    serializers = {
        'list':    ListDocumentSerializer,
        'retrieve':  RetrieveDocumentSerializer,
    }

    queryset = Document.objects.all()


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
