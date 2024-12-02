from asgiref.sync import sync_to_async
from django.contrib.auth import alogin
from django.contrib.auth.decorators import login_not_required
from django.http import HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django_htmx.http import HttpResponseClientRedirect
from payments.asaas.asaas_api import AsaasApi

from accounts.forms import SigninForm, SignupForm


@method_decorator(login_not_required, name='dispatch')
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


@method_decorator(login_not_required, name='dispatch')
class SigninView(View):
    template_name = 'accounts/signin.html'
    form_class = SigninForm

    async def get(self, request: HttpRequest):
        await AsaasApi.tasks.delete_all_customers()
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

        redirect_url = request.GET.get('next', '')
        return HttpResponseClientRedirect(
            redirect_url if redirect_url else reverse('home')
        )


class SignoutView(View):
    async def post(self, request: HttpRequest):
        await alogin(request, None)
        return HttpResponseClientRedirect(reverse('signin'))
