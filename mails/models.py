from django.contrib.auth.models import User
from django.db import models


class EmailProviderEnum(models.TextChoices):
    GMAIL = 'Gmail', 'gmail.com'
    YANDEX = 'Yandex', 'yandex.ru'
    MAIL = 'Mail.ru', 'mail.ru'


class EmailAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mails')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    provider = models.CharField(max_length=50, choices=EmailProviderEnum.choices)
    count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} -- {self.email}'


class EmailMessage(models.Model):
    uid = models.IntegerField()
    subject = models.CharField(max_length=255, verbose_name="Тема сообщения")
    sent_date = models.DateTimeField(verbose_name="Дата отправки", blank=True, null=True)
    received_date = models.DateTimeField(verbose_name="Дата получения", blank=True, null=True)
    message_text = models.TextField(verbose_name="Текст сообщения")
    attachments = models.JSONField(verbose_name="Список прикреплённых файлов", blank=True, null=True)
    email_account = models.ForeignKey(EmailAccount, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject