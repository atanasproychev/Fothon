# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_topic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('text', models.CharField(max_length=500)),
                ('author', models.ForeignKey(to_field='user_ptr', to='forum.ForumUser')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('topic', models.ForeignKey(to_field='id', to='forum.Topic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='forumuser',
            name='categories',
            field=models.ManyToManyField(to='forum.Category'),
            preserve_default=True,
        ),
    ]
