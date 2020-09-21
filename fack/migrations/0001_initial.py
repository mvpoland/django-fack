# -*- coding: utf-8 -*-
from django.db import models, migrations
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(help_text='The actual question itself.', verbose_name='question')),
                ('answer', models.TextField(help_text='The answer text.', verbose_name='answer', blank=True)),
                ('slug', models.SlugField(max_length=100, verbose_name='slug')),
                ('status', models.IntegerField(default=0, help_text="Only questions with their status set to 'Active' will be displayed. Questions marked as 'Group Header' are treated as such by views and templates that are set up to use them.", verbose_name='status', choices=[(1, 'Active'), (0, 'Inactive'), (2, 'Group Header')])),
                ('protected', models.BooleanField(default=False, help_text='Set true if this question is only visible by authenticated users.', verbose_name='is protected')),
                ('sort_order', models.IntegerField(default=0, help_text='The order you would like the question to be displayed.', verbose_name='sort order')),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='created on')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='updated on')),
                ('nr_views', models.IntegerField(default=0)),
                ('created_by', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='+', verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['sort_order', 'nr_views', 'created_on'],
                'verbose_name': 'Frequent asked question',
                'verbose_name_plural': 'Frequently asked questions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuestionScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.IntegerField(default=1, verbose_name='score', choices=[(0, b'No'), (1, b'Yes')])),
                ('ip_address', models.IPAddressField(null=True, verbose_name='IP address', blank=True)),
                ('question', models.ForeignKey(on_delete=models.deletion.CASCADE, to='fack.Question')),
                ('user', models.ForeignKey(on_delete=models.deletion.CASCADE, default=-1, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150, verbose_name='name')),
                ('slug', models.SlugField(max_length=150, verbose_name='slug')),
                ('sort_order', models.IntegerField(default=0, help_text='The order you would like the topic to be displayed.', verbose_name='sort order')),
                ('nr_views', models.IntegerField(default=0)),
                ('icon', models.ImageField(null=True, upload_to=b'topic_icons/', blank=True)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now, verbose_name='created on', auto_now_add=True)),
                ('updated_on', models.DateTimeField(default=datetime.datetime.now, verbose_name='updated on', auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='+', verbose_name='created by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('site', models.ForeignKey(on_delete=models.deletion.CASCADE, blank=True, to='sites.Site', null=True)),
                ('updated_by', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='+', verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['sort_order', 'nr_views', 'name'],
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='questions', verbose_name='topic', to='fack.Topic'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='question',
            name='updated_by',
            field=models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='+', verbose_name='updated by', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
