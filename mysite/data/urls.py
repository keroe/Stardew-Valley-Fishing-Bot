from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^download/', views.download, name='download'),
    url(r'^ranking/', views.model_form_upload, name='ranking'),
    url(r'^help/', views.data, name='help'),
]
