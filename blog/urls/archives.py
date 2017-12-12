"""Urls for the blog archives"""
from django.conf.urls import url

from blog.views.archives import PostDay
from blog.views.archives import PostMonth
from blog.views.archives import PostYear

year_patterns = [
    url(r'^(?P<year>\d{4})/$',
        PostYear.as_view(),
        name='post_archive_year'),
    url(r'^(?P<year>\d{4})/page/(?P<page>\d+)/$',
        PostYear.as_view(),
        name='post_archive_year_paginated'),
]

month_patterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/$',
        PostMonth.as_view(),
        name='post_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/page/(?P<page>\d+)/$',
        PostMonth.as_view(),
        name='post_archive_month_paginated'),
]

day_patterns = [
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/$',
        PostDay.as_view(),
        name='post_archive_day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/page/(?P<page>\d+)/$',
        PostDay.as_view(),
        name='post_archive_day_paginated'),
]

archive_patterns = (year_patterns + month_patterns + day_patterns )

urlpatterns = archive_patterns
