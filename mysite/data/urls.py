from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^ranking/$', views.ranking, name='ranking'),
    url(r'^help/', views.data, name='help'),
	url(r'^ranking/upload$', views.upload, name='upload'),

]
