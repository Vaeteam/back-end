# Generated by Django 4.0.6 on 2022-10-01 08:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('address', models.CharField(max_length=150)),
                ('fee', models.PositiveIntegerField()),
                ('duration', models.PositiveIntegerField(default=0)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('note', models.TextField(blank=True, null=True)),
                ('state', models.CharField(choices=[('Đang chờ xử lí', 'Đang chờ xử lí'), ('Bài post của bạn không hợp lệ', 'Bài post của bạn không hợp lệ'), ('Đã xử lí, bài post của bạn đã đăng lên bảng tin', 'Đã xử lí, bài post của bạn đã đăng lên bảng tin'), ('Gia sư và bạn đã liên hệ với nhau thành công', 'Gia sư và bạn đã liên hệ với nhau thành công'), ('Gia sư đã dạy xong môn học bạn yêu cầu', 'Gia sư đã dạy xong môn học bạn yêu cầu')], max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('-date_posted',),
            },
        ),
        migrations.CreateModel(
            name='PostReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('score', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('time', models.DateTimeField()),
                ('is_edited', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RangeTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)], max_length=10)),
                ('time_begin', models.TimeField()),
                ('time_end', models.TimeField()),
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
