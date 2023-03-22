import json
from typing import Dict, Union

import django.middleware.csrf
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, JsonResponse
from django.shortcuts import render

from src.models import AnchorAcPass, ChairmanAcPass, AnchorInfo, ChairmanInfo, Employment
from src.util import create_default_anchor, create_default_chairman, employed_to_dict


def login(request):
    if request.method == 'POST':
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
    else:
        return HttpResponseServerError(500)


def get_csrf_token(request):
    django.middleware.csrf.get_token(request)
    return HttpResponse('success')


def register(request):
    if request.method == 'POST':
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
    else:
        return HttpResponseServerError(500)


def set_base_info(request):
    if request.method == 'POST':
        user_info = request.POST
        if user_info['type'] == 'anchor':
            AnchorInfo.objects.filter(account=user_info['account']).update(nickname=user_info['nickname'])
            AnchorInfo.objects.filter(account=user_info['account']).update(sex=user_info['sex'])
        else:
            ChairmanInfo.objects.filter(account=user_info['account']).update(nickname=user_info['nickname'])
            ChairmanInfo.objects.filter(account=user_info['account']).update(sex=user_info['sex'])
        return HttpResponse('success')
    else:
        return HttpResponseServerError(500)


def get_user_info(request):
    if request.method == 'GET':
        account = request.GET['account']
        src_type = request.GET['type']
        if src_type == 'anchor':
            info = AnchorInfo.objects.get(account=account)
            json.dumps(info)
            object_info = {
                'account': info.account,
            }
            return JsonResponse(object_info)
        else:
            info = ChairmanInfo.objects.get(account=account)
            sex = '男' if info.sex == 0 else '女'
            result = [
                {'name': '昵称', 'attributes': info.nickname},
                {'name': '性别', 'attributes': sex},
                {'name': '电话号码', 'attributes': info.telephone_number},
                {'name': '简介', 'attributes': info.introduction},
            ]
            json_result = json.dumps(result)
        return HttpResponse(json_result)
    else:
        return HttpResponseServerError(500)


def update_user_info(request):
    if request.method == 'POST':
        # TODO Find the Relation in the database and update it.
        user_info = request.POST
        if user_info['type'] == 'anchor':
            orm = AnchorInfo.objects.filter(account=user_info['account'])
        else:
            orm = ChairmanInfo.objects.filter(account=user_info['account'])

        # change the attribute by the param
        attr_name = user_info['attr_name']
        attributes = user_info['attributes']
        if attr_name == 'nickname':
            orm.update(nickname=attributes)
            return HttpResponse('success')
        elif attr_name == 'sex':
            # sex need be defined in the front side
            orm.update(sex=int(attributes))
            return HttpResponse('success')
        elif attr_name == 'telephone_number':
            orm.update(telephone_number=attributes)
            return HttpResponse('success')
        elif attr_name == 'introduction':
            orm.update(introduction=attributes)
            return HttpResponse('success')
        return HttpResponseBadRequest(400)
    else:
        return HttpResponseServerError(500)


def get_employed_anchor(request):
    if request.method == 'POST':
        # the function need to return all employee and the length of employed by POST conference
        employed_length = 0
        employee_list = []
        post_info = request.POST
        conference_account = post_info['account']
        employed_list = Employment.objects.filter(administer=conference_account)
        for employed_data in employed_list:
            anchor_info = AnchorInfo.objects.get(account=employed_data.anchor)
            employee_list.append(employed_to_dict(employed_data, anchor_info))
        json_result = json.dumps(employee_list)
        return HttpResponse(json_result)
    else:
        return HttpResponseServerError(500)
