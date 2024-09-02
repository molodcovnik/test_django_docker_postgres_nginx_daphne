# Generated by Django 5.1 on 2024-08-29 10:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField()),
                ('subject', models.CharField(max_length=255, verbose_name='Тема сообщения')),
                ('sent_date', models.DateTimeField(verbose_name='Дата отправки')),
                ('received_date', models.DateTimeField(blank=True, null=True, verbose_name='Дата получения')),
                ('message_text', models.TextField(verbose_name='Текст сообщения')),
                ('attachments', models.JSONField(blank=True, null=True, verbose_name='Список прикреплённых файлов')),
                ('email_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mails.emailaccount')),
            ],
        ),
    ]
