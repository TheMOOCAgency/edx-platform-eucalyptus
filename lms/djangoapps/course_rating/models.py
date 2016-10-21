"""
Author: Naresh Makwana
"""
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg

from model_utils.models import TimeStampedModel

from openedx.core.djangoapps.xmodule_django.models import CourseKeyField


class CourseRating(TimeStampedModel):
    """
    Keeps course wise student course progress.
    """
    class Meta(object):
        app_label = "course_rating"
        unique_together = (('student', 'course_id'),)

    course_id = CourseKeyField(max_length=255, db_index=True, verbose_name='Course ID')

    student = models.ForeignKey(User, db_index=True)

    stars = models.FloatField(default=0.0)

    @classmethod
    def calc_avg_ratings(cls, course_id):
        """
        Calculates the average ratings for the course.
        """
        avg_stars = cls.objects.filter(course_id=course_id).aggregate(Avg('stars')).values()[0]
        if not avg_stars:
            avg_stars = 0.0
        return round(avg_stars * 2) / 2

    @classmethod
    def has_rated(cls, course_id, student_id):
        """
        Calculates the average ratings for the course.
        """
        return cls.objects.filter(course_id=course_id, student_id=student_id).count() > 0

    def __repr__(self):
        return 'CourseRating<%r>' % ({
            'course_id': self.course_id,
            'student_id': self.student_id,
            'stars': str(self.stars),
        },)

    def __unicode__(self):
        return unicode(repr(self))
