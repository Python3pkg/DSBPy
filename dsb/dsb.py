import requests

from dsb.network import available_plans
from dsb.parser import parse_plan


class DSB:
    def __init__(self, username, password):
        '''
        Initialize DSB

        :param username: username for DSB
        :type username: str

        :param password: password for DSB
        :type password: str
        '''
        self.username = username
        self.password = password

    @property
    def plans(self):
        '''
        Receive and parse available plans for username and password

        :return: parsed available plans
        :rtype: [dsb.parser.Plan]
        '''
        plans = available_plans(self.username, self.password)
        return [
            parse_plan(requests.get(plan_url).text)
            for plan_url in plans
        ]
