from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.abouturls, name='about'),
        url(r'^detail/(?P<item_id>\d+)/$', views.detail, name='detail'),
]
