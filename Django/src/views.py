import django.middleware.csrf
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render

from src.models import AnchorAcPass, ChairmanAcPass


# Create your views here.


def login(request):
    user_info = request.POST
    if user_info['type'] == 'anchor':
        valid = AnchorAcPass.objects.filter(account=user_info['account'])
        if valid.exists():
            if not valid.values('password')[0]['password'] == user_info['password']:
                return HttpResponseBadRequest(400)
        else:
            return HttpResponseBadRequest(400)
    else:
        valid = ChairmanAcPass.objects.filter(account=user_info['account'])
        if valid.exists():
            if not valid.values('password')[0]['password'] == user_info['password']:
                return HttpResponseBadRequest(400)
        else:
            return HttpResponseBadRequest(400)
    return HttpResponse('success')


def get_csrf_token(request):
    django.middleware.csrf.get_token(request)
    return HttpResponse('success')


def register(request):
    user_info = request.POST
    if user_info['type'] == 'anchor':
        if not AnchorAcPass.objects.filter(account=user_info['account']).exists():
            AnchorAcPass.objects.create(account=user_info['account'], password=user_info['password'])
        else:
            return HttpResponseBadRequest(400)
    else:
        if not ChairmanAcPass.objects.filter(account=user_info['account']).exists():
            ChairmanAcPass.objects.create(account=user_info['account'], password=user_info['password'])
        else:
            return HttpResponseBadRequest(400)
    return HttpResponse('success')
