import math
from typing import List, Optional
from models import Team, Match


class BracketBase:
    def __init__(self, teams: List[Team]):
        self.teams = teams
        self.rounds: List[List[Match]] = []
        self.completed = False
        self.champion: Optional[Team] = None
        self.type_name = "Base"

    def generate(self):
        raise NotImplementedError

    def advance(self, match: Match):
        raise NotImplementedError

    def is_ready_to_start(self):
        return all(t.checked_in for t in self.teams)

    def all_rounds_completed(self) -> bool:
        return all(m.status == "Completed" for rnd in self.rounds for m in rnd)
