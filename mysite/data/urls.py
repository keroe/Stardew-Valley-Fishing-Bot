from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^download/', views.download, name='download'),
    url(r'^ranking/', views.ranking, name='ranking'),
    url(r'$', views.data, name='data'),
]
