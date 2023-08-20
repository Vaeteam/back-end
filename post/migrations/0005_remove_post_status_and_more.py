# Generated by Django 4.2 on 2023-08-20 12:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0004_poststatus_remove_requestteaching_learner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='status',
        ),
        migrations.RemoveField(
            model_name='poststatus',
            name='last_update_time',
        ),
        migrations.AddField(
            model_name='poststatus',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='poststatus',
            name='post',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='post.post'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poststatus',
            name='selected_teacher',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='poststatus',
            name='state',
            field=models.CharField(choices=[('created', 'Tạo bài thành công'), ('verified', 'Bài đã được duyệt'), ('verified_failed', 'Bài tuyển bị không hợp lệ'), ('edited', 'Bài tuyển đã chỉnh sửa'), ('teacher_selected', 'Đã chọn được giáo viên'), ('learner_request', 'Học viên mời dạy'), ('teacher_accepted', 'Giáo viên đã đồng ý'), ('teacher_rejected ', 'Giáo viên đã từ chối'), ('connected', 'Đã kết nối giáo viên và học viên')], default='created', max_length=100),
        ),
    ]
