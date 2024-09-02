from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import EmailAccountSerializer, EmailMessageSerializer
from mails.models import EmailAccount, EmailMessage
from mails.services.fetch_emails import get_messages
from mails.services.fetch_mails_mail_ru import get_messages_mail


class UserEmailsApiView(generics.GenericAPIView):
    serializer_class = EmailAccountSerializer

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')
        if not user_id:
            return Response([], status=status.HTTP_200_OK)

        user = User.objects.get(id=user_id)
        mails = user.mails.all()

        # Проверяем, есть ли связанные аккаунты
        if not mails.exists():
            return Response([], status=status.HTTP_200_OK)

        # Сериализуем и возвращаем данные
        serializer = self.get_serializer(mails, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmailMessagesApiView(APIView):
    serializer_class = EmailMessageSerializer

    def get(self, request, account_id):
        try:
            account = EmailAccount.objects.get(id=account_id)
        except EmailAccount.DoesNotExist:
            account = None

        mails = EmailMessage.objects.filter(email_account=account).order_by('-sent_date')


        serializer = self.serializer_class(instance=mails, many=True)
        return Response(serializer.data, status=200)


@api_view(['GET'])
def fetch_emails(request, account_id):
    account = get_object_or_404(EmailAccount, pk=account_id)
    username = account.email
    password = account.password
    try:
        if account.get_provider_display() == 'mail.ru':
            get_messages_mail(account_id, username, password)
        else:
            get_messages(account_id, username, password, account.get_provider_display()
)
        return Response({
            'status': 'success',
            'message': 'Загрузка сообщений началась',
        }, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response({
            'status': 'error',
            'message': str(e),
        }, status=status.HTTP_400_BAD_REQUEST)