# -- coding: UTF-8 --
from braces.views import SetHeadlineMixin
from notifications.views import AllNotificationsList, UnreadNotificationsList

from blog.views.mixins.view_mixins import PaginationMixin


class AllNotificationsListView(PaginationMixin, SetHeadlineMixin, AllNotificationsList):
    headline = '通知'
    paginate_by = 20
    prefetch_related = ('actor', 'target')


class UnreadNotificationsListView(PaginationMixin, SetHeadlineMixin, UnreadNotificationsList):
    headline = '未读通知'
    paginate_by = 20
    prefetch_related = ('actor', 'target')
