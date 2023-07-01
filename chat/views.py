from django.shortcuts import render

# Create your views here.

from chat.models import Room
from django.views.generic import TemplateView

class Home(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        # 단순히 시작히 룸을 만들기 위한 장치
        Room.objects.get_or_create(name='노티룸', group_name='main')
        return super().get(request, *args, **kwargs)
