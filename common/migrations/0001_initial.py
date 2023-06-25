# Generated by Django 4.2 on 2023-05-31 15:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RangeTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('available_day', models.CharField(choices=[('mon', 'Thứ 2'), ('tue', 'Thứ 3'), ('wed', 'Thứ 4'), ('thu', 'Thứ 5'), ('fri', 'Thứ 6'), ('sat', 'Thứ 7'), ('sun', 'Chủ Nhật')], max_length=50)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('parent_subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.subject')),
            ],
        ),
    ]
