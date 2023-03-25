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
        'working_status': False if anchor_data.workingstatus == 0 else True,
        'working_time_percent': "%.2f" % percentage if percentage < 100 else 100
    }
    return result
