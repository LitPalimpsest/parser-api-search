from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'collections', views.CollectionViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'pages', views.PageViewSet)
router.register(r'sentences', views.SentenceViewSet)
router.register(r'locations', views.LocationViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'litlong.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'api.views.home', name='home'),
    url(r'^search/document/(?P<document_id>\d+)', 'api.views.document',
        name='document'),
    url(r'^search/', 'api.views.search', name='search'),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
