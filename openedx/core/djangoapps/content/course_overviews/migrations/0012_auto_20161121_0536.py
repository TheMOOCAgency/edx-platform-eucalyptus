# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0011_courseoverview_visible_to_manager_only'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseoverview',
            name='enrollment_workflow',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='courseoverview',
            name='subject',
            field=models.TextField(default=b'demo', max_length=255),
        ),
    ]
