"""
Api for getting final grades of the user.

Author: Chintan Joshi
"""
from django.db import transaction
from student.models import User 

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from edx_rest_framework_extensions.authentication import JwtAuthentication

from openedx.core.lib.api.view_utils import view_auth_classes
from openedx.core.lib.api.authentication import (
    SessionAuthenticationAllowInactiveUser,
    OAuth2AuthenticationAllowInactiveUser,
)

from opaque_keys.edx.locations import SlashSeparatedCourseKey

from lms.djangoapps.grades.new.course_grade import CourseGradeFactory

from courseware.courses import get_course_with_access


authentication_classes = (
    OAuth2AuthenticationAllowInactiveUser, 
    SessionAuthenticationAllowInactiveUser, 
    JwtAuthentication
)
permission_classes = (permissions.IsAuthenticated,)

@view_auth_classes()
@transaction.non_atomic_requests
@api_view()
def get_final_grades(request, course_id):
    """
    **Use Cases**

        Retrieve final grade of the user.

    **Example Requests**:

        GET: /final_grades/course_id
    
        GET: /final_grades/course-v1:test+test111+2014_T3

    **Returns**:

        Course_id: id of the course

        User: current user

        Grade: Final Grade of the user

        Error: If any error persists

    """
    if request.user.is_authenticated():
        user = request.user

        try:
            course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
            course = get_course_with_access(user, 'load', course_key, depth=None)
        except Exception as e:
            return Response(
                data={
                "Error": e.message
            })

        try:
            course_grade = CourseGradeFactory(user).create(course, read_only=False)
            grade_summary = course_grade.summary
            return Response(
                data={
                "User": request.user.username,
                "Course ID": course_id,
                "Grade": grade_summary.get('percent')
            })
        except Exception as e:
            return Response(
                data={
                "Error": e.message
            })
    else:
        return Response(
            data={
            "Error":"Authentication credentials were not provided."
        })