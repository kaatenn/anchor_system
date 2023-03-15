import django.middleware.csrf
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import render

from src.models import AnchorAcPass, ChairmanAcPass, AnchorInfo, ChairmanInfo
from src.util import create_default_anchor, create_default_chairman


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
            create_default_anchor(user_info)
        else:
            return HttpResponseBadRequest(400)
    else:
        if not ChairmanAcPass.objects.filter(account=user_info['account']).exists():
            create_default_chairman(user_info)
        else:
            return HttpResponseBadRequest(400)
    return HttpResponse('success')


def set_nick_name(request):
    user_info = request.POST
    if user_info['type'] == 'anchor':
        AnchorInfo.objects.filter(account=user_info['account']).update(nickname=user_info['nickname'])
    else:
        ChairmanInfo.objects.filter(account=user_info['account']).update(nickname=user_info['nickname'])
    return HttpResponse('success')


def get_user_info(request):
    return HttpResponseBadRequest(400)
