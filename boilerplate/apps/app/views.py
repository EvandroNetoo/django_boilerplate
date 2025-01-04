from django.http import HttpRequest
from django.shortcuts import render
from django.views import View


class HomeView(View):
    template_name = 'app/home.html'

    async def get(self, request: HttpRequest):
        return render(request, self.template_name)
