from django.conf.urls import include
from django.conf.urls import url

app_name = 'blog'
urlpatterns = [
    url(r'^', include('blog.urls.urls')),
    url(r'^archives/', include('blog.urls.archives')),
]
