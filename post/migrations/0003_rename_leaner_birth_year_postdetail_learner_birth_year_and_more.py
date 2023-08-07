# Generated by Django 4.2 on 2023-08-07 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_rename_fee_postdetail_teaching_fee_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postdetail',
            old_name='leaner_birth_year',
            new_name='learner_birth_year',
        ),
        migrations.RenameField(
            model_name='postdetail',
            old_name='leaner_name',
            new_name='learner_name',
        ),
        migrations.RenameField(
            model_name='postdetail',
            old_name='leaner_sex',
            new_name='learner_sex',
        ),
        migrations.RenameField(
            model_name='postdetail',
            old_name='reuqest_teacher_sex',
            new_name='request_teacher_sex',
        ),
        migrations.RenameField(
            model_name='postdetail',
            old_name='reuqest_teacher_year_old_from',
            new_name='request_teacher_year_old_from',
        ),
        migrations.RenameField(
            model_name='postdetail',
            old_name='reuqest_teacher_year_old_to',
            new_name='request_teacher_year_old_to',
        ),
        migrations.AlterField(
            model_name='postdetail',
            name='teaching_address',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
