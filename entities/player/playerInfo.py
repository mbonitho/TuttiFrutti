
from settings import *


class PlayerInfo:

    def __init__(self):

        self.current_day = 0
        self.base_daily_income = 1000
        self.current_income = self.base_daily_income
        self.total_income = -self.base_daily_income