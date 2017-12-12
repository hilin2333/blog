# -*- coding: utf-8 -*-
"""Calendar module for blog"""
from __future__ import absolute_import

from calendar import HTMLCalendar
from datetime import date

from django.core.urlresolvers import reverse
from django.utils.dates import MONTHS
from django.utils.formats import date_format

from blog.models import Post

from django.utils.translation import ugettext_lazy as _

AMERICAN_TO_EUROPEAN_WEEK_DAYS = [6, 0, 1, 2, 3, 4, 5]

WEEKDAYS_ZH = {
    0: _('一'), 1: _('二'), 2: _('三'), 3: _('四'), 4: _('五'),
    5: _('六'), 6: _('日')
}


class Calendar(HTMLCalendar):
    """
    Extension of the HTMLCalendar.
    """

    def __init__(self):
        """
        Retrieve and convert the localized first week day
        http://www.17sucai.com/pins/demoshow/24573
        at initialization,use sta as the first day of a week
        """
        HTMLCalendar.__init__(self, AMERICAN_TO_EUROPEAN_WEEK_DAYS[0])

    def formatday(self, day, weekday):
        """
        Return a day as a table cell with a link
        if entries are published this day.
        """
        if day and day in self.day_entries:
            day_date = date(self.current_year, self.current_month, day)
            archive_day_url = reverse('blog:post_archive_day',
                                      args=[day_date.strftime('%Y'),
                                            day_date.strftime('%m'),
                                            day_date.strftime('%d')])
            return '<div class ="td_%d on" onclick="location.href= \'%s\'">%d' \
                   '</div>' % (weekday + 1, archive_day_url, day)

        return self.showday(day, weekday)

    def formatweekday(self, day):
        """
        Return a weekday name translated as a table header.
        """
        return '<div class="th_%d bold">%s</div>' % (day + 1,
                                                     WEEKDAYS_ZH[day].title())

    def formatweekheader(self):
        """
        Return a header for a week as a table row.
        """
        s = ''.join(self.formatweekday(i) for i in self.iterweekdays())
        value = '<div class="sign_row">%s</div>' % s
        return value

    def formatfooter(self, previous_month, next_month):
        """
        Return a footer for a previous and next month.
        """
        footer = '<tfoot><tr>' \
                 '<td colspan="3" class="prev">%s</td>' \
                 '<td class="pad">&nbsp;</td>' \
                 '<td colspan="3" class="next">%s</td>' \
                 '</tr></tfoot>'
        if previous_month:
            previous_content = '<a href="%s" class="previous-month">%s</a>' % (
                reverse('blog:post_archive_month', args=[
                    previous_month.strftime('%Y'),
                    previous_month.strftime('%m')]),
                date_format(previous_month, 'YEAR_MONTH_FORMAT'))
        else:
            previous_content = '&nbsp;'

        if next_month:
            next_content = '<a href="%s" class="next-month">%s</a>' % (
                reverse('blog:post_archive_month', args=[
                    next_month.strftime('%Y'),
                    next_month.strftime('%m')]),
                date_format(next_month, 'YEAR_MONTH_FORMAT'))
        else:
            next_content = '&nbsp;'

        return footer % (previous_content, next_content)

    def formatmonthname(self, theyear, themonth, withyear=True):
        """Return a month name translated as a table row."""
        monthname = '%s%s%s' % (theyear, '年', MONTHS[themonth].title())
        return '<div class="sign_succ_calendar_title"><div class="calendar_month_span">%s</div></div>' % monthname

    def formatmonth(self, theyear, themonth, withyear=True,
                    previous_month=None, next_month=None):
        """
        Return a formatted month as a table
        with new attributes computed for formatting a day,
        and thead/tfooter.
        """
        self.current_year = theyear
        self.current_month = themonth
        postFilter = Post.objects.filter(
            status=1,
            pub_date__year=theyear,
            pub_date__month=themonth
        ).datetimes('pub_date', 'day')
        self.day_entries = [date.day for date in postFilter]
        v = []
        a = v.append
        a('<div class="sign_main" id="sign_layer">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a('<div class="sign_equal" id="sign_cal">')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week))
            a('\n')
        # a('\n')
        # a(self.formatfooter(previous_month, next_month))
        a('\n')
        a('</div>')
        a('\n')
        a('</div>')
        return ''.join(v)

    def formatweek(self, week):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd) for (d, wd) in week)
        return '<div class="sign_row">%s</div>' % s

    def showday(self, day, weekday):
        """
        Return a day as a table cell.
        """
        if day == 0:
            return '<div class="td_%d calendar_record">&nbsp;&nbsp;</div>' % (weekday + 1)  # day outside month
        else:
            return '<div class="td_%d calendar_record">%d</div>' % (weekday + 1, day)
