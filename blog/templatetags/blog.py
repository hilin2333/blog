# -*- coding: utf-8 -*-
from django.template import Library

from datetime import date
from django.conf import settings
from ..models import Post,Tag
from django.utils import timezone
from ..calendar import Calendar

register = Library()

@register.inclusion_tag('blog/tags/dummy.html', takes_context=True)
def get_calendar_entries(context, year=None, month=None,
                         template='blog/tags/posts_calendar.html'):
    """
    Return an HTML calendar of entries.
    """
    if not (year and month):
        day_week_month = (context.get('day') or
                          context.get('week') or
                          context.get('month'))
        pub_date = getattr(context.get('object'),
                                   'pub_date', None)
        if day_week_month:
            current_month = day_week_month
        elif pub_date:
            if settings.USE_TZ:
                pub_date = timezone.localtime(pub_date)
            current_month = pub_date.date()
        else:
            today = timezone.now()
            if settings.USE_TZ:
                today = timezone.localtime(today)
            current_month = today.date()
        current_month = current_month.replace(day=1)
    else:
        current_month = date(year, month, 1)
    dates = list(map(
        lambda x: settings.USE_TZ and timezone.localtime(x).date() or x.date(),
        Post.objects.filter(status=1).datetimes('pub_date', 'month')))

    if current_month not in dates:
        dates.append(current_month)
        dates.sort()
    index = dates.index(current_month)

    previous_month = index > 0 and dates[index - 1] or None
    next_month = index != len(dates) - 1 and dates[index + 1] or None
    calendar = Calendar()

    return {'template': template,
            'next_month': next_month,
            'previous_month': previous_month,
            'calendar': calendar.formatmonth(
                current_month.year,
                current_month.month,
                previous_month=previous_month,
                next_month=next_month)}


@register.simple_tag()
def get_tags():

    return Tag.objects.filter(post__status=1)
