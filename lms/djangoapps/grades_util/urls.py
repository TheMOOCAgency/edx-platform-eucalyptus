from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns(
    'grades_util.views',

    url(
        r'^assignment_passing_status/{}/(?P<section_id>[^/]*)/$'.format(
            settings.COURSE_ID_PATTERN
        ),
        'assignment_passing_status',
        name='assignment_passing_status'
    ),
)

#Final Grades api
if settings.FEATURES.get('TMA_ENABLE_FINAL_GRADES_API'):
    urlpatterns += (
        url(
            r'^final_grades/{}/$'.format(
                settings.COURSE_ID_PATTERN,
            ),
            'grades_util.api.get_final_grades',
            name='grades_api'
        ),
    )
