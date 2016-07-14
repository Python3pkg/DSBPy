import requests
from bs4 import BeautifulSoup

url = 'https://iphone.dsbcontrol.de/iPhoneService.svc/DSB'


class InvalidLogin(Exception):
    pass


class Change:
    '''
    High-level-obj to simplify access to a change
    '''
    def __init__(self, raw_change):
        self.type, self.lesson, self.teacher, self.subject, self.room, \
            self.comment = raw_change

    def __str__(self):
        return '<{}: {}.h {} (bei {}) @{} | {}>'.format(
            self.type, self.lesson, self.subject,
            self.teacher, self.room, self.comment
        )

    def __repr__(self):
        return self.__str__()


class Announcement:
    pass


def _receive_raw_plans(username, password):
    '''
    fetch raw plans from DSBControl-dash
    '''
    login_r = requests.get(
        url + '/authid/{}/{}'.format(username, password)
    ).text.replace('"', '')
    if login_r == '00000000-0000-0000-0000-000000000000':
        raise InvalidLogin()
    plans_r = requests.get(url + '/timetables/{}'.format(login_r)).json()
    return [
        requests.get(plan_r['timetableurl']).text for plan_r in plans_r
    ]


def _parse_table(raw_table):
    '''
    parse plan-tables, returns (plan-title, {class: [change_obj, ..]})
    '''
    soup = BeautifulSoup(raw_table, 'html.parser')
    title = soup.find(class_='mon_title')
    if not title:
        # invalid plan
        return
    # first line is <thead> => skip
    rows = soup.find('table', class_='mon_list').find_all('tr')[1:]
    plan = {}
    last_title = None
    for row in rows:
        header = row.find('td', class_='inline_header')
        if header:
            last_title = header.text.replace('  ', ' ')
            plan[last_title] = []
        else:
            data = [td.text for td in row.find_all('td')]
            if len(data) == 1:
                # it's an announcement
                # that's currently not implemented
                pass
            elif len(data) > 1:
                plan[last_title].append(Change(data))
            else:
                del plan[last_title]
    return title.text, plan


def get_plans(username, password):
    '''
    helper-func to fetch dash, extract tables and parse them
    '''
    raw_plans = _receive_raw_plans(username, password)
    plan_data = [_parse_table(raw_plan) for raw_plan in raw_plans]
    r = {}
    for title, data in plan_data:
        r[title] = data
    return r
