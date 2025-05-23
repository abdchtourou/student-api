# Generated by Django 4.2.21 on 2025-05-15 11:44

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
        ('todoList', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='todo',
            options={'ordering': ['-created_at'], 'verbose_name': 'Todo', 'verbose_name_plural': 'Todos'},
        ),
        migrations.AddField(
            model_name='todo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, help_text='When the task was last updated', verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, help_text='When the task was created', verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='description',
            field=models.TextField(blank=True, help_text='Optional detailed description of the task', verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='is_completed',
            field=models.BooleanField(default=False, help_text='Whether the task has been completed', verbose_name='Completed'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='student',
            field=models.ForeignKey(help_text='The student who owns this task', on_delete=django.db.models.deletion.CASCADE, related_name='todos', to='student.student', verbose_name='Student'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.CharField(help_text='Title of the task (3-100 characters)', max_length=100, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Title'),
        ),
        migrations.AddIndex(
            model_name='todo',
            index=models.Index(fields=['student', '-created_at'], name='todoList_to_student_35e119_idx'),
        ),
        migrations.AddIndex(
            model_name='todo',
            index=models.Index(fields=['is_completed'], name='todoList_to_is_comp_adae78_idx'),
        ),
    ]
