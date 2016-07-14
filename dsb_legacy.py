import requests
from bs4 import BeautifulSoup

url = 'https://mobile.dsbcontrol.de/DSBmobilePage.aspx'
url_no_content = \
        'https://light.dsbcontrol.de/DSBlightWebsite/Homepage/NoContent.htm'


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


def _extract_viewstate(soup):
    '''
    extracts __VIEWSTATE and __VIEWSTATEGENERATOR from `soup`
    '''
    viewstate_element = soup.find('input', id='__VIEWSTATE')
    viewstate = viewstate_element['value']
    viewstategenerator_element = soup.find('input', id='__VIEWSTATEGENERATOR')
    viewstategenerator = viewstategenerator_element['value']
    return viewstate, viewstategenerator


def _receive_raw_dash(username, password):
    '''
    login to DSBControl and fetch raw-dashboard
    '''
    with requests.Session() as session:
        start = session.get(
            url
        )
        viewstate, viewstategenerator = _extract_viewstate(
            BeautifulSoup(start.text, 'html.parser')
        )
        login1 = session.post(
            url, data={
                'ctl03$txtUserName': username,
                'ctl03$txtPassword': password,
                'ctl03$btnLogin': 'Login',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': viewstategenerator
            })
        login1_soup = BeautifulSoup(login1.text, 'html.parser')
        login2 = session.post(
            url, data={
                'ctl03$txtUserName': username,
                'ctl03$txtPassword': '',
                'UserName': login1_soup.find('input', id='UserName')['value'],
                'IsAuthenticated': 'true',
                '__VIEWSTATE': viewstate,
                '__VIEWSTATEGENERATOR': viewstategenerator
            })
        return login2.text


def _receive_raw_plans(raw_dash):
    '''
    fetch raw plans from DSBControl-dash
    '''
    soup = BeautifulSoup(raw_dash, 'html.parser')
    raw_iframes = soup.find_all('iframe')
    return [
        requests.get(raw_iframe['src']).text for raw_iframe in raw_iframes
        if raw_iframe['src'] != url_no_content
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
    # first line is thead => skip
    rows = soup.find('table', class_='mon_list').find_all('tr')[1:]
    plan = {}
    last_title = None
    for row in rows:
        header = row.find('td', class_='inline_header')
        if header:
            last_title = header.text
            plan[last_title] = []
        else:
            data = [td.text for td in row.find_all('td')]
            if len(data) >= 1:
                plan[last_title].append(Change(data))
            else:
                del plan[last_title]
    return title.text, plan


def get_plans(username, password):
    '''
    helper-func to fetch raw-dash, extract tables and parse them
    '''
    raw_dash = _receive_raw_dash(username, password)
    raw_plans = _receive_raw_plans(raw_dash)
    plan_data = [_parse_table(raw_plan) for raw_plan in raw_plans]
    r = {}
    for title, data in plan_data:
        r[title] = data
    return r
