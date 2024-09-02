import json

from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from mails.forms import EmailAccountForm
from mails.models import EmailAccount, EmailMessage


def index(request):
    if request.user.is_authenticated:
        mails = EmailMessage.objects.filter(email_account__user=request.user)
        accounts = EmailAccount.objects.filter(user=request.user)
        context = {
            'mails': mails,
            'accounts': accounts,
            "user_id": mark_safe(json.dumps(request.user.id)),
        }
        return render(request, "mails/index.html", context=context)
    return render(request, "mails/index.html")


class EmailAccountListView(ListView):
    model = EmailAccount
    template_name = 'mails/email_accounts.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return EmailAccount.objects.filter(user=self.request.user)


class EmailAccountCreateView(CreateView):
    form_class = EmailAccountForm
    model = EmailAccount
    template_name = 'mails/email_account_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class EmailAccountDetailView(DetailView):
    model = EmailAccount
    template_name = 'mails/email_account_detail.html'
    context_object_name = "account"

    def get_success_url(self, **kwargs):
        return reverse_lazy('account-detail', kwargs={'pk': self.get_object().id})


class EmailAccountDeleteView(DeleteView):
    model = EmailAccount
    template_name = 'mails/email_account_delete.html'
    success_url = reverse_lazy('accounts')
    context_object_name = 'account'


def email_feed(request, account_id):
    return render(request, "mails/email_feed.html", {
        "account_id": mark_safe(json.dumps(account_id)),
        })

