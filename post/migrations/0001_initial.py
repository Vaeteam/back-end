# Generated by Django 4.0.1 on 2023-04-15 06:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppliedTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage', models.CharField(max_length=100)),
                ('t_create', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_create', models.DateTimeField(null=True)),
                ('date_posted', models.DateTimeField(null=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='PostDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('address', models.CharField(max_length=150)),
                ('fee', models.PositiveIntegerField()),
                ('note', models.TextField(blank=True, null=True)),
                ('duration', models.PositiveIntegerField(default=0)),
                ('state', models.CharField(choices=[('Đang chờ xử lí', 'Đang chờ xử lí'), ('Bài post của bạn không hợp lệ', 'Bài post của bạn không hợp lệ'), ('Đã xử lí, bài post của bạn đã đăng lên bảng tin', 'Đã xử lí, bài post của bạn đã đăng lên bảng tin'), ('Gia sư và bạn đã liên hệ với nhau thành công', 'Gia sư và bạn đã liên hệ với nhau thành công'), ('Gia sư đã dạy xong môn học bạn yêu cầu', 'Gia sư đã dạy xong môn học bạn yêu cầu')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PostReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('t_create', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_edited', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RangeTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_create', models.DateTimeField(default=django.utils.timezone.now)),
                ('day', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)])),
                ('t_begin', models.TimeField()),
                ('t_end', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='RequestTeaching',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_create', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
