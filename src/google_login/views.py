from django.http import HttpResponse
from django.views import View

from django.shortcuts import render
from mainsite.models import User

from google.oauth2 import id_token
from google.auth.transport import requests

from decouple import config

# заготовка на будущее
class GoogleTokenSignInView(View):
	def post(self, request):
		pass
