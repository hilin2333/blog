from django.conf.urls import url

from rest import views

urlpatterns = [
    url(r'^upload/', views.UploadList.as_view(),name='upload'),
]