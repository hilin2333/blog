# -*- coding: utf-8 -*-
"""Views for Zinnia archives"""
import datetime

from django.views.generic.dates import BaseDayArchiveView
from django.views.generic.dates import BaseMonthArchiveView
from django.views.generic.dates import BaseYearArchiveView

from blog.models import Post
from blog.views.mixins.archives import ArchiveMixin
from blog.views.mixins.archives import PreviousNextPublishedMixin
from blog.views.mixins.templates import \
    PostQuerysetArchiveTemplateResponseMixin


class PostArchiveMixin(ArchiveMixin,
                        PreviousNextPublishedMixin,
                        PostQuerysetArchiveTemplateResponseMixin):
    """
    Mixin combinating:

    - ArchiveMixin configuration centralizing conf for archive views.
    - PrefetchCategoriesAuthorsMixin to prefetch related objects.
    - PreviousNextPublishedMixin for returning published archives.
    - CallableQueryMixin to force the update of the queryset.
    - PostQuerysetArchiveTemplateResponseMixin to provide a
      custom templates for archives.
    """
    queryset = Post.objects.filter(status=1)

class PostYear(PostArchiveMixin, BaseYearArchiveView):
    """
    View returning the archives for a year.
    """
    make_object_list = True
    headline = '归档'
    model = Post
    template_name_suffix = '_archive_year'


class PostMonth(PostArchiveMixin, BaseMonthArchiveView):
    """
    View returning the archives for a month.
    """
    headline = '归档'
    model = Post
    template_name_suffix = '_archive_month'


class PostDay(PostArchiveMixin, BaseDayArchiveView):
    """
    View returning the archive for a day.
    """
    headline = '归档'
    model = Post
    template_name_suffix = '_archive_day'