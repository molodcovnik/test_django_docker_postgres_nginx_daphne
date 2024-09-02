from django.urls import path
from mails.views import index, EmailAccountCreateView, EmailAccountListView, EmailAccountDetailView, EmailAccountDeleteView, email_feed

urlpatterns = [
    path('', index, name='home'),
    path('<int:account_id>/', email_feed, name='feed'),
    path('email-accounts/', EmailAccountListView.as_view(), name='accounts'),
    path('email-accounts/create/', EmailAccountCreateView.as_view(), name='account-create'),
    path('email-accounts/<int:pk>/', EmailAccountDetailView.as_view(), name='account-detail'),
    path('email-accounts/<int:pk>/delete', EmailAccountDeleteView.as_view(), name='account-delete'),
]