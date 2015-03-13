from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'collections', views.CollectionViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'litlong.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
)
