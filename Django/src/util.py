import json

from src.models import ChairmanAcPass, ChairmanInfo, AnchorAcPass, AnchorInfo


def create_default_anchor(user_info):
    AnchorAcPass.objects.create(account=user_info['account'], password=user_info['password'])
    AnchorInfo.objects.create(account=AnchorAcPass.objects.get(account=user_info['account']),
                              nickname=user_info['account'],
                              introduction=None,
                              sex=0,
                              telephone_number=None)
    return


def create_default_chairman(user_info):
    ChairmanAcPass.objects.create(account=user_info['account'], password=user_info['password'])
    ChairmanInfo.objects.create(account=ChairmanAcPass.objects.get(account=user_info['account']),
                                nickname=user_info['account'],
                                introduction=None,
                                sex=0,
                                telephone_number=None)
    return


def employed_to_dict(anchor_data, anchor_info):
    percentage = anchor_data.worktime / anchor_data.goaltime * 100
    result = {
        'anchor_account': anchor_data.anchor_id,
        'anchor_nickname': anchor_info.nickname,
        'salary': "%d" % anchor_data.salary,
        'working_status': False if anchor_data.workingstatus == 0 else True,
        'working_time_percent': "%.2f" % percentage if percentage < 100 else 100
    }
    return result


def get_result_list(info):
    sex = '男' if info.sex == 0 else '女'
    result = [
        {'name': '昵称', 'attributes': info.nickname},
        {'name': '性别', 'attributes': sex},
        {'name': '电话号码', 'attributes': info.telephone_number},
        {'name': '简介', 'attributes': info.introduction},
    ]
    return result


def conference_to_dict(conference_data, conference_info):
    percentage = conference_data.worktime / conference_data.goaltime * 100
    result = {
        'chairman_account': conference_data.administer_id,
        'chairman_nickname': conference_info.nickname,
        'salary': "%d" % conference_data.salary,
        'working_status': False if conference_data.workingstatus == 0 else True,
        'working_time_percent': "%.2f" % percentage if percentage < 100 else 100
    }
    return result


def waiting_conference_to_list(conferences):
    result = []
    for conference_data in conferences:
        result.append({
            'account': conference_data.account_id,
            'nickname': conference_data.nickname,
            'telephone_number': conference_data.telephone_number,
            'introduction': conference_data.introduction
        })
    return result


def wanting_anchor_to_list(wanting_data, anchor_data):
    sex = '男' if anchor_data.sex == 0 else '女'
    result = {
        'account': anchor_data.account_id,
        'nickname': anchor_data.nickname,
        'sex': sex,
        'telephone_number': anchor_data.telephone_number,
        'introduction': anchor_data.introduction,
        'salary': wanting_data.wanted_salary,
        'salary_fluctuation': wanting_data.wanted_salary_fluctuation,
        'time': wanting_data.wanted_goal_time,
        'time_fluctuation': wanting_data.wanted_goal_time_fluctuation
    }
    return result
