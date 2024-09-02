from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync
from mails.models import EmailAccount


def update_account_count(account_id, messages_length):
    email_account = EmailAccount.objects.get(id=account_id)
    # email_account.count += 1
    email_account.count = messages_length
    email_account.save()

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f'account_{account_id}', {
            'type': 'count_message',
            'message': {
                'id': email_account.id,
                'email': email_account.email,
                'provider': email_account.provider,
                'count': email_account.count,
            }
        }
    )
# from mails.services.counter import update_account_count


