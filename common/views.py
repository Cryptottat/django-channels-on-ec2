from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AutoUser

# Create your views here.
class AppLogin(APIView):
    def post(self, request):
        user_id = request.data.get('user_id', "")
        user_pw = request.data.get('user_pw', "")
        user = AutoUser.objects.filter(user_id=user_id).first()
        if user is None:
            return Response(dict(msg="noid"))
        # if check_password(user_pw, user.user_pw): # for encrypted pass
        if user_pw == user.user_pw: # for text password
            return Response(dict(msg="ok"))
        else:
            return Response(dict(msg="fail"))