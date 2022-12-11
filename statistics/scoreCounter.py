from settings import *

class ScoreCounter:

    def __init__(self):
        self.good = 0
        self.bad = 0
        self.missed = 0

    
    def get_day_score(self):
        return (self.good * GOOD_ARREST_BONUS) - (self.bad * BAD_ARREST_PENALTY) - (self.missed * MISSED_ARREST_PENALTY)