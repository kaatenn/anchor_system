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
    result = {
        'anchor_account': anchor_data.anchor,
        'anchor_nickname': anchor_info.nickname,
        'working_status': anchor_data.workingstatus,
        'working_time_percent': anchor_data.worktime / anchor_data.goaltime
    }
    return result
