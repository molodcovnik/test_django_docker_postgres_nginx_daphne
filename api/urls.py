from django.urls import path
from api.views import UserEmailsApiView, EmailMessagesApiView, fetch_emails


urlpatterns = [
    path('<int:account_id>/', fetch_emails),
    path('emails/', UserEmailsApiView.as_view()),
    path('emails/<int:account_id>/', EmailMessagesApiView.as_view()),
]