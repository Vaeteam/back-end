# Generated by Django 4.2 on 2023-08-19 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0003_rename_leaner_birth_year_postdetail_learner_birth_year_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(choices=[('created', 'Tạo bài thành công'), ('verified', 'Bài đã được duyệt'), ('teacher_selected', 'Đã chọn được giáo viên'), ('teacher_accepted', 'Giáo viên đã đồng ý'), ('teacher_rejected ', 'Giáo viên đã từ chối'), ('connected', 'Đã kết nối giáo viên và học viên')], default='created', max_length=100)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_update_time', models.DateTimeField(blank=True, null=True)),
                ('selected_teacher', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='requestteaching',
            name='learner',
        ),
        migrations.RemoveField(
            model_name='requestteaching',
            name='post',
        ),
        migrations.RemoveField(
            model_name='requestteaching',
            name='teacher',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='updated_date',
            new_name='last_update_time',
        ),
        migrations.RemoveField(
            model_name='post',
            name='state',
        ),
        migrations.AlterField(
            model_name='postdetail',
            name='learner_sex',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('any', 'any')], max_length=6),
        ),
        migrations.AlterField(
            model_name='postdetail',
            name='request_teacher_sex',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('any', 'any')], max_length=6),
        ),
        migrations.DeleteModel(
            name='AppliedTeacher',
        ),
        migrations.DeleteModel(
            name='RequestTeaching',
        ),
        migrations.AddField(
            model_name='post',
            name='status',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='post.poststatus'),
            preserve_default=False,
        ),
    ]
