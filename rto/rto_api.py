from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from .models import RTOadmin ,  Vehicle , Rules
from datetime import *
from police.models import Police
import json
from django.http import JsonResponse

def validate_username_api(request):
    data = json.loads(request.body)
    username = data['username']

    usernametaken = Police.objects.filter(police_username=username).count()
    if usernametaken:
        return JsonResponse({'username_error': 'username already in use.'})
    return JsonResponse({'username_valid': True})
