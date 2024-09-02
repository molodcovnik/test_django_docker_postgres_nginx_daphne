from django.contrib import admin

from mails.models import EmailAccount, EmailMessage


admin.site.register(EmailAccount)
admin.site.register(EmailMessage)
