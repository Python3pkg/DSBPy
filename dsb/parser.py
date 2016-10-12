from bs4 import BeautifulSoup

from dsb.exceptions import InvalidPlan


class Change:
    def __init__(self, type, lesson, subject, teacher, room, comment):
        self.type = type
        self.lesson = lesson
        self.subject = subject
        self.teacher = teacher
        self.room = room
        self.comment = comment

    def __repr__(self):
        return '<{}: {}.h {} (bei {}) @{} | {}>'.format(
            self.type, self.lesson, self.subject,
            self.teacher, self.room, self.comment
        )


class Announcement:
    pass


def parse_plan(raw_plan):
    '''
    Parse plan from raw data (raw_plan)

    :param raw_plan: raw plan-data
    :type raw_plan: str

    :return: Plan-title and extracted changes
    :rtype: (str, [dsb.parser.Change])
    '''
    soup = BeautifulSoup(raw_plan, 'html.parser')
    title = soup.find(class_='mon_title')
    if not title:
        raise InvalidPlan()
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
                # it's an announcement => currently not implemented
                pass
            elif len(data) > 1:
                plan[last_title].append(Change(*data))
            else:
                del plan[last_title]
    return title.text, plan
