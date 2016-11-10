"""
Grades utilities
"""
from courseware.model_data import FieldDataCache, ScoresClient
from util.db import outer_atomic
from lms.djangoapps.grades.new.course_grade import CourseGradeFactory
from django.db import transaction
from student.models import User

from opaque_keys.edx.locations import SlashSeparatedCourseKey
from courseware.courses import get_course_with_access

def has_passed(request, course_id, section_url_name):
    """
    Returns True if the student has higher or equeal grades in
    asssignment type.
    """
    student = request.user

    # Get the course by ID
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)
    course = get_course_with_access(student, 'load', course_key, depth=None)

    course_grade = CourseGradeFactory(student).create(course, read_only=False)
    grade_summary = course_grade.summary

    # Get assignment type wise percent
    assignments = {}
    for section in grade_summary['section_breakdown']:
        if section.get('prominent', False):
            assignments.update({
                section['category']: section['percent']
            })

    # Get the section assignment type
    section_assignment_type = ''
    for chapter in course.get_children():
        for sequenctial in chapter.get_children():
            if sequenctial.url_name == section_url_name:
                section_assignment_type = sequenctial.format
                break

    # Get section assignment percent
    percentage = assignments.get(section_assignment_type, 0.0)

    # Return passing status
    return percentage * 100 == 100
