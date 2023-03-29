import json
from random import randint

import django.middleware.csrf
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError, QueryDict
from django.utils.datetime_safe import datetime

from src.models import AnchorAcPass, ChairmanAcPass, AnchorInfo, ChairmanInfo, Employment, Wanting
from src.util import create_default_anchor, create_default_chairman, employed_to_dict, get_result_list, \
    conference_to_dict, waiting_conference_to_list, wanting_anchor_to_list


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
            result = get_result_list(info)

        else:
            info = ChairmanInfo.objects.get(account=account)
            result = get_result_list(info)
            if info.is_waiting == 1:
                is_waiting = '开启'
            else:
                is_waiting = '关闭'
            result.append({'name': '开启招募', 'attributes': is_waiting})
        json_result = json.dumps(result)
        return HttpResponse(json_result)
    else:
        return HttpResponseServerError(500)


def update_user_info(request):
    if request.method == 'POST':
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
        elif attr_name == 'is_waiting':
            orm.update(is_waiting=int(attributes))
            return HttpResponse('success')
        return HttpResponseBadRequest(400)
    else:
        return HttpResponseServerError(500)


def get_employed_anchor(request):
    if request.method == 'POST':
        # the function need to return all employee who was employed by the conference of the account
        result_list = []
        post_info = request.POST
        conference_account = post_info['account']
        employed_list = Employment.objects.filter(administer=conference_account)
        for employed_data in employed_list:
            anchor_info = AnchorInfo.objects.get(account=employed_data.anchor)
            result_list.append(employed_to_dict(employed_data, anchor_info))
        json_result = json.dumps(result_list)
        return HttpResponse(json_result)
    else:
        return HttpResponseServerError(500)


def dismiss(request):
    if request.method == 'DELETE':
        delete = QueryDict(request.body)
        relation = Employment.objects.filter(anchor=delete['anchor_account'], administer=delete['conference_account'])
        relation.delete()
        return HttpResponse('success')
    else:
        return HttpResponseServerError(500)


def get_employer(request):
    if request.method == 'POST':
        result_list = []
        anchor_info = request.POST
        anchor_account = anchor_info['account']
        conference_list = Employment.objects.filter(anchor=anchor_account)
        for conference_data in conference_list:
            conference_info = ChairmanInfo.objects.get(account=conference_data.administer)
            result_list.append(conference_to_dict(conference_data, conference_info))
        json_result = json.dumps(result_list)
        return HttpResponse(json_result)
    else:
        return HttpResponseServerError(500)


def living(request):
    if request.method == 'POST':
        post = request.POST
        anchor_account = post['anchor_account']
        conference_account = post['chairman_account']
        employment = Employment.objects.filter(anchor=anchor_account, administer=conference_account)
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        employment.update(workingstatus=1, start_time=time)
        return HttpResponse('success')
    else:
        return HttpResponseServerError(500)


def end_living(request):
    if request.method == 'POST':
        post = request.POST
        anchor_account = post['anchor_account']
        conference_account = post['chairman_account']
        employment = Employment.objects.filter(anchor=anchor_account, administer=conference_account)
        if len(employment) != 1:
            return HttpResponseBadRequest(400)
        new_time = datetime.now()
        origin_time = employment[0].start_time.replace(tzinfo=new_time.tzinfo)
        time_diff = new_time - origin_time
        minutes_diff = time_diff.total_seconds() // 60
        worktime = employment[0].worktime + minutes_diff
        employment.update(workingstatus=0, worktime=worktime, start_time=None)
        return HttpResponse('success')
    else:
        return HttpResponseServerError(500)


def get_random_conference(request):
    if request.method == 'GET':
        account = request.GET['account']
        employment_records = Employment.objects.filter(anchor__account=account)
        chairman_accounts = [emp.administer.account for emp in employment_records]
        waiting_conference = ChairmanInfo.objects.exclude(account__in=chairman_accounts).filter(is_waiting=1)
        last = waiting_conference.count()
        result_list = []
        if last <= 2:
            result = waiting_conference_to_list(waiting_conference)
            json_result = json.dumps(result)
            return HttpResponse(json_result)
        else:
            count = 0
            indexes = [-1, -1, -1]
            while count < 2:
                num = randint(0, last - 1)
                try:
                    indexes.index(num)
                except ValueError:
                    indexes[count] = num
                    result_list.append(waiting_conference[num])
                    count += 1
            result = waiting_conference_to_list(result_list)
            json_result = json.dumps(result)
            return HttpResponse(json_result)
    else:
        return HttpResponseServerError(500)


def wanting(request):
    if request.method == 'POST':
        wanting_info = request.POST
        Wanting.objects.create(
            anchor=AnchorAcPass.objects.get(account=wanting_info['anchor_account']),
            administer=ChairmanAcPass.objects.get(account=wanting_info['chairman_account']),
            wanted_salary=int(wanting_info['wanted_salary']),
            wanted_salary_fluctuation=int(wanting_info['wanted_salary_fluctuation']),
            wanted_goal_time=int(wanting_info['wanted_goal_time']),
            wanted_goal_time_fluctuation=int(wanting_info['wanted_goal_time_fluctuation'])
        )
        return HttpResponse('success')
    else:
        return HttpResponseServerError(500)


def get_waiting_employee(request):
    if request.method == 'GET':
        account = request.GET['account']
        wanting_list = Wanting.objects.filter(administer=ChairmanAcPass.objects.get(account=account))
        result = []
        for wanting_data in wanting_list:
            anchor_data = AnchorInfo.objects.get(account=AnchorAcPass.objects.get(account=wanting_data.anchor_id))
            result.append(wanting_anchor_to_list(wanting_data, anchor_data))
        json_result = json.dumps(result)
        return HttpResponse(json_result)
    else:
        return HttpResponseServerError(500)


def add_employment(request):
    if request.method == 'POST':
        employment = request.POST
        Wanting.objects.get(anchor=AnchorAcPass.objects.get(account=employment['anchor_account']),
                            administer=ChairmanAcPass.objects.get(
                                account=employment['chairman_account'])).delete()
        Employment.objects.create(
            administer=ChairmanAcPass.objects.get(account=employment['chairman_account']),
            anchor=AnchorAcPass.objects.get(account=employment['anchor_account']),
            goaltime=employment['time'],
            salary=employment['salary'],
            workingstatus=0,
            worktime=0,
            start_time=None
        )
        return HttpResponse('success')
    else:
        return HttpResponseServerError(500)


def refuse_wanting(request):
    if request.method == 'DELETE':
        employment = QueryDict(request.body)
        Wanting.objects.get(anchor=AnchorAcPass.objects.get(account=employment['anchor_account']),
                            administer=ChairmanAcPass.objects.get(
                                account=employment['chairman_account'])).delete()
        return HttpResponse('success')
    else:
        return HttpResponseServerError(500)
