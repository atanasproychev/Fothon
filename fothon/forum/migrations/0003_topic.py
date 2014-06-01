# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_category_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('author', models.ForeignKey(to_field='user_ptr', to='forum.ForumUser')),
                ('category', models.ForeignKey(to_field='id', to='forum.Category')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('last_modified_from', models.ForeignKey(to_field='user_ptr', to='forum.ForumUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
