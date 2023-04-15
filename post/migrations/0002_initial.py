# Generated by Django 4.0.1 on 2023-04-15 06:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import post.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('post', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subject',
            name='parent_subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='post.subject'),
        ),
        migrations.AddField(
            model_name='requestteaching',
            name='learner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_learner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requestteaching',
            name='post',
            field=models.ForeignKey(on_delete=post.models.Post, to='post.post'),
        ),
        migrations.AddField(
            model_name='requestteaching',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_teacher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='rangetime',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='range_time', to='post.post'),
        ),
        migrations.AddField(
            model_name='rangetime',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='range_time_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postreview',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='post_review', to='post.post'),
        ),
        migrations.AddField(
            model_name='post',
            name='approve_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approve_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='post_detail',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='post.postdetail'),
        ),
        migrations.AddField(
            model_name='post',
            name='subjects',
            field=models.ManyToManyField(to='post.Subject'),
        ),
        migrations.AddField(
            model_name='post',
            name='teachers',
            field=models.ManyToManyField(blank=True, related_name='teachers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appliedteacher',
            name='post',
            field=models.ForeignKey(on_delete=post.models.Post, to='post.post'),
        ),
        migrations.AddField(
            model_name='appliedteacher',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]