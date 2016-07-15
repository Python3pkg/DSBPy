import requests

from dsb.network import available_plans
from dsb.parser import parse_plan


class DSB:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @property
    def plans(self):
        plans = available_plans(self.username, self.password)
        return [
            parse_plan(requests.get(plan_url).text)
            for plan_url in plans
        ]
