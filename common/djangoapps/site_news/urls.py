from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns(
    'site_news.views',

    url(r'^detail/(?P<news_id>[0-9]*)/$', 'news_detail', name='news_detail'),
    url(r'^$', 'news', name='news_list'),
)

if settings.FEATURES.get('TMA_ENABLE_PLATFORM_WIDE_NEWS_API'):
    from site_news.api import APINewsPages
    urlpatterns += patterns(
        'site_news.api',
        url(r'^api/list/$', APINewsPages.as_view()),
        url(r'^api/detail/(?P<news_id>[0-9]*)$', APINewsPages.as_view()),
    )
