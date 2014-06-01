# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumUser',
            fields=[
                ('user_ptr', models.OneToOneField(serialize=False, auto_created=True, primary_key=True, to_field='id', to=settings.AUTH_USER_MODEL)),
                ('picture', models.ImageField(upload_to='', null=True, blank=True)),
                ('gender', models.CharField(max_length=1, null=True, choices=[('M', 'Male'), ('F', 'Female')])),
                ('city', models.CharField(max_length=50, null=True)),
                ('birth_date', models.DateField(null=True)),
            ],
            options={
                'verbose_name_plural': 'users',
                'abstract': False,
                'verbose_name': 'user',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('order', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
