from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns(
    'enrollment_workflow.views',

    url(
        r'^enrollment_workflow/$',
        'workflow',
        name='enrollment_workflow'
    ),
    url(
        r'^request_granted/{}/(?P<student_id>[^/]*)/$'.format(
            settings.COURSE_ID_PATTERN
        ),
        'granted',
        name='enrollment_workflow_granted'
    ),
    url(
        r'^request_rejected/{}/(?P<student_id>[^/]*)/$'.format(
            settings.COURSE_ID_PATTERN
        ),
        'rejected',
        name='enrollment_workflow_rejected'
    ),
)
