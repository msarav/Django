from django.conf.urls import url
from . import views

urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^login/$', views.user_login, name='login'),
        url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^about/$', views.abouturls, name='about'),
        url(r'^detail/(?P<item_id>\d+)/$', views.detail, name='detail'),
        url(r'^suggestions/', views.suggestions, name='suggestion'),
        url(r'^newitem/', views.newitem, name='newitem'),
        url(r'^myitems/', views.myitems, name='myitems'),
        url(r'^searchlib/', views.searchlib, name='searchlib'),

]
