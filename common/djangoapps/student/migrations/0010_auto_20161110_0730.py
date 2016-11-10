# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0009_userprofile_is_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='identity_proof_file_extension',
            field=models.CharField(max_length=4, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='identity_proof_uploaded_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
