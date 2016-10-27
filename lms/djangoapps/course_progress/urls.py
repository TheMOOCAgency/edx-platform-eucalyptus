from django.conf.urls import include, patterns, url
from django.conf import settings

from course_progress.api import APICompletionProgress


urlpatterns = patterns(
    '',
    url(
        r'^track_html_component/$',
        'course_progress.custom_track.track_html_component',
        name='track_html_component'
    ),
)

# Course progress API
if settings.FEATURES.get('TMA_ENABLE_COMPLETION_TRACKING_API'):
    urlpatterns += (
        url(
            r'^api/?$',
            APICompletionProgress.as_view(),
            name='completion_progress',
        ),
        url(
            r'^api/(?P<chapter>[^/]*)/$',
            APICompletionProgress.as_view(),
            name='completion_progress_chapter',
        ),
        url(
            r'^api/(?P<chapter>[^/]*)/(?P<section>[^/]*)/$',
            APICompletionProgress.as_view(),
            name='completion_progress_section',
        ),
        url(
            r'^api/(?P<chapter>[^/]*)/(?P<section>[^/]*)/(?P<unit>[^/]*)/?$',
            APICompletionProgress.as_view(),
            name='completion_progress_unit',
        ),
    )

# Whether to show green dots on course nav
if settings.FEATURES.get('TMA_SHOW_COMPLETION_ON_COURSEWARE_NAVIGATION'):
    urlpatterns += (
        url(
            r'^completion_status/$',
            'course_progress.views.get_completion_status',
            name='completion_status'
        ),
    )

# Whether to show tracking percent on dashboard
if settings.FEATURES.get('TMA_SHOW_COMPLETION_ON_DASHBOARD'):
    urlpatterns += (
        url(
            r'^overall_course_progress/',
            'course_progress.views.get_overall_course_progress',
            name='get_overall_course_progress'
        ),
    )
