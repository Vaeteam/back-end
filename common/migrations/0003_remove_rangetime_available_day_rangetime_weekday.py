# Generated by Django 4.2 on 2023-08-06 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_alter_rangetime_available_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rangetime',
            name='available_day',
        ),
        migrations.AddField(
            model_name='rangetime',
            name='weekday',
            field=models.CharField(choices=[('Thứ Hai', 'Thứ Hai'), ('Thứ Ba', 'Thứ Ba'), ('Thứ Tư', 'Thứ Tư'), ('Thứ Năm', 'Thứ Năm'), ('Thứ Sáu', 'Thứ Sáu'), ('Thứ Bảy', 'Thứ Bảy'), ('Chủ Nhật', 'Chủ Nhật')], default=0, max_length=50),
            preserve_default=False,
        ),
    ]
