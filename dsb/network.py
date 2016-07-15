import requests

from dsb.exceptions import InvalidLogin

api = 'https://iphone.dsbcontrol.de/iPhoneService.svc/DSB'


def available_plans(username, password):
    timetable_id = requests.get(
        api + '/authid/{}/{}'.format(username, password)
    ).text.replace('"', '')
    if timetable_id == '00000000-0000-0000-0000-000000000000':
        raise InvalidLogin()
    return [
        timetable['timetableurl']
        for timetable in requests.get(
            api + '/timetables/{}'.format(timetable_id)
        ).json()
    ]
