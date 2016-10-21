from django.views.decorators.csrf import ensure_csrf_cookie
from django.db import IntegrityError
from django.http import JsonResponse

from opaque_keys.edx.locations import SlashSeparatedCourseKey

from student.models import CourseEnrollment

from course_rating.models import CourseRating


@ensure_csrf_cookie
def course_ratings_handler(request, course_id):
    """
    Description: This view kept for rating the course.

    Arguments:
        course_id: course ID for which rating needs to be set.

    Request Parameters:
        stars: float, indicates out of 5 stars

    Returns:
        json response with newly calculated course rating average.

    Assumes the course_id is in a valid format.

    Author: Naresh Makwana
    """
    course_key = SlashSeparatedCourseKey.from_deprecated_string(course_id)

    if request.method == "POST":
        # Get the parameters from POST
        stars = request.POST.get('stars', 0.0)
        # save the course ratings
        try:
            course_rating = CourseRating.objects.create(student=request.user, course_id=course_key, stars=stars)
        except IntegrityError:
            pass

    # re-calculate the average course ratings
    avg_ratings = CourseRating.calc_avg_ratings(course_id=course_key)

    # return json response
    return JsonResponse({
        'avg_ratings': avg_ratings,
        'can_rate': CourseEnrollment.is_enrolled(request.user, course_key) and \
            not CourseRating.has_rated(student_id=request.user.id, course_id=course_key)
    })
