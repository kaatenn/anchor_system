from src.models import ChairmanAcPass, ChairmanInfo, AnchorAcPass, AnchorInfo


def create_default_anchor(user_info):
    """
       Creates a new AnchorAcPass and AnchorInfo object using the given user_info.

       Args:
           user_info (dict): A dictionary containing the user information.

       Returns:
           None
    """
    # Create a new AnchorAcPass object
    AnchorAcPass.objects.create(account=user_info['account'], password=user_info['password'])

    # Create a new AnchorInfo object
    AnchorInfo.objects.create(account=AnchorAcPass.objects.get(account=user_info['account']),
                              nickname=user_info['account'],
                              introduction=None,
                              sex=0,
                              telephone_number=None)

    # Return None
    return


def create_default_chairman(user_info):
    """
       Creates a new ChairmanAcPass and ChairmanInfo object using the given user_info.

       Args:
           user_info (dict): A dictionary containing the user information.

       Returns:
           None
    """
    # Create a new ChairmanAcPass object
    ChairmanAcPass.objects.create(account=user_info['account'], password=user_info['password'])

    # Create a new ChairmanInfo object
    ChairmanInfo.objects.create(account=ChairmanAcPass.objects.get(account=user_info['account']),
                                nickname=user_info['account'],
                                introduction=None,
                                sex=0,
                                telephone_number=None)

    return


def employed_to_dict(anchor_data, anchor_info):
    """
        Converts the given AnchorData and AnchorInfo objects to a dictionary format.

        Args:
            anchor_data (AnchorData): An AnchorData object.
            anchor_info (AnchorInfo): An AnchorInfo object.

        Returns:
            dict: A dictionary containing the converted information.
    """
    # Calculate the percentage of worktime to goaltime
    percentage = anchor_data.worktime / anchor_data.goaltime * 100

    # Create a dictionary with the converted information
    result = {
        'anchor_account': anchor_data.anchor_id,
        'anchor_nickname': anchor_info.nickname,
        'salary': "%d" % anchor_data.salary,
        'working_status': False if anchor_data.workingstatus == 0 else True,
        'working_time_percent': "%.2f" % percentage if percentage < 100 else 100
    }

    return result


def get_result_list(info):
    """
        Creates a list of dictionaries, where each dictionary represents an attribute of the input object.

        Args:
            info: An instance of AnchorInfo or ChairmanInfo model.

        Returns:
            An instance of AnchorInfo or ChairmanInfo model.
    """
    # Convert the 'sex' attribute to a string ('男' if 0, '女' otherwise)
    sex = '男' if info.sex == 0 else '女'

    # Create a list of dictionaries containing the attribute names and their values
    result = [
        {'name': '昵称', 'attributes': info.nickname},
        {'name': '性别', 'attributes': sex},
        {'name': '电话号码', 'attributes': info.telephone_number},
        {'name': '简介', 'attributes': info.introduction},
    ]
    return result


def conference_to_dict(conference_data, conference_info):
    """
        Converts the given ConferenceData and ConferenceInfo objects to a dictionary format.

        Args:
            conference_data: An AnchorData object.
            conference_info: An AnchorInfo object

        Returns:
            dict: A dictionary containing the converted information.
    """
    # Calculate the percentage of worktime to goaltime
    percentage = conference_data.worktime / conference_data.goaltime * 100

    # Create a dictionary with the converted information
    result = {
        'chairman_account': conference_data.administer_id,
        'chairman_nickname': conference_info.nickname,
        'salary': "%d" % conference_data.salary,
        'working_status': False if conference_data.workingstatus == 0 else True,
        'working_time_percent': "%.2f" % percentage if percentage < 100 else 100
    }
    return result


def waiting_conference_to_list(conferences):
    """
    Converts the given Conference objects to a list format.

    Params:
        conferences: a list of ConferenceWait objects.

    Returns:
        result: a list of dictionaries, each containing information about a waiting
    """
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
    """
        Convert wanting anchor data and anchor info to a dictionary for API response

        Params:
            wanting_data: A wanting data object containing information about the desired salary and work hours of the anchor.
            anchor_data: An anchor data object containing information about the anchor.

        Returns:
            A dictionary containing the following information about the anchor
    """
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
