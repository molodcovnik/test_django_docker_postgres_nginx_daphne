from rest_framework import serializers

from mails.models import EmailAccount, EmailMessage


class EmailAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailAccount
        fields = ['email', 'provider', ]


class EmailMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmailMessage
        fields = ['uid', 'subject', 'sent_date', 'received_date', 'message_text', 'attachments', ]
