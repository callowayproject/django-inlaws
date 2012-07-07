from django.conf.urls.defaults import patterns, url
from blog.models import Post

from django.views.generic.dates import (ArchiveIndexView, YearArchiveView,
                                        MonthArchiveView, DayArchiveView,
                                        DateDetailView)

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(),
        {'queryset': Post.objects.published(), 'date_field': 'publish'},
        name='blog_detail'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$',
        DayArchiveView.as_view(),
        {'queryset': Post.objects.published(), 'date_field': 'publish'},
        name='blog_archive_day'
    ),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',
        MonthArchiveView.as_view(),
        {'queryset': Post.objects.published(), 'date_field': 'publish'},
        name='blog_archive_month'
    ),
    url(r'^(?P<year>\d{4})/$',
        YearArchiveView.as_view(),
        {'queryset': Post.objects.published(), 'date_field': 'publish'},
        name='blog_archive_year'
    ),
    url(r'^$',
        ArchiveIndexView.as_view(),
        {'queryset': Post.objects.published()},
        name='blog_index'
    ),
)
