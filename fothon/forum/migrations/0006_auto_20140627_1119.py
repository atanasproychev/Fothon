# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20140623_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.CharField(max_length=1, default='R', choices=[('R', 'Regular'), ('S', 'Special')]),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='forumuser',
            name='categories',
        ),
    ]
