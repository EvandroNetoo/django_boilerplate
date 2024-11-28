import logging

from asgiref.sync import sync_to_async
from django.contrib.auth import alogin
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django_htmx.http import HttpResponseClientRedirect

from accounts.forms import SigninForm, SignupForm

logger = logging.getLogger(__name__)


class SignupView(View):
    template_name = 'accounts/signup.html'
    form_class = SignupForm

    async def get(self, request: HttpRequest):
        context = {
            'form': self.form_class(),
        }
        return render(request, self.template_name, context)

    async def post(self, request: HttpRequest):
        form = self.form_class(request.POST)
        if not await sync_to_async(form.is_valid)():
            context = {
                'form': form,
            }
            return render(request, 'components/form.html', context)

        user = await sync_to_async(form.save)()
        await alogin(request, user)

        return HttpResponseClientRedirect(reverse('home'))


class SigninView(View):
    template_name = 'accounts/signin.html'
    form_class = SigninForm

    async def get(self, request: HttpRequest):
        context = {
            'form': self.form_class(),
        }
        return render(request, self.template_name, context)

    async def post(self, request: HttpRequest):
        form = self.form_class(request, request.POST)
        if not await sync_to_async(form.is_valid)():
            context = {
                'form': form,
            }

            return render(request, 'components/form.html', context)

        await alogin(request, form.get_user())

        return HttpResponseClientRedirect(reverse('home'))
