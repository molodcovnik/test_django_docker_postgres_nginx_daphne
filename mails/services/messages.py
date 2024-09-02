from mails.models import EmailMessage, EmailAccount
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from mails.services.counter import update_account_count


def create_new_email_message(account_id, uid, subject, sent_date, received_date, message_text, attachments):
    email_account = EmailAccount.objects.get(id=account_id)
    message = EmailMessage.objects.create(
        email_account=email_account,
        uid=uid,
        subject=subject,
        sent_date=sent_date,
        received_date=received_date,
        message_text=message_text,
        attachments=attachments
    )

    # Уведомляем всех участников группы через WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'email_{account_id}', {
            'type': 'chat_message',
            'message': {
                'uid': message.uid,
                'subject': message.subject,
                'sent_date': message.sent_date.strftime("%Y-%m-%d %H:%M:%S") if message.sent_date else None,
                'received_date': message.received_date.strftime("%Y-%m-%d %H:%M:%S") if message.received_date else None,
                'message_text': message.message_text,
                'attachments': message.attachments,
            }
        }
    )

    # update_account_count(account_id)
# from django.utils import timezone
# from mails.services.messages import create_new_email_message
# create_new_email_message(2, 121212, 'Input JS', timezone.now(), timezone.now(), 'Третье сокет сообщение', ['file.pdf', 'file2.txt'])
