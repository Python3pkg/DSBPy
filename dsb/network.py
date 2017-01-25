import requests

from dsb.exceptions import InvalidLogin

API_URL = 'https://iphone.dsbcontrol.de/iPhoneService.svc/DSB'


def available_plans(username, password):
    '''
    Receive available plans for `username` and `password`

    :param username: username for DSB
    :type username: str

    :param password: password for DSB
    :type password: str

    :return: List of URLs to available plans
    :rtype: [str]
    '''
    timetable_id = requests.get(
        API_URL + '/authid/{}/{}'.format(username, password)
    ).text.replace('"', '')
    if timetable_id == '00000000-0000-0000-0000-000000000000':
        raise InvalidLogin()
    return [
        timetable['timetableurl']
        for timetable in requests.get(
            API_URL + '/timetables/{}'.format(timetable_id)
        ).json()
    ]
