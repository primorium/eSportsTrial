import uuid
import math
from models import Team, Match
from brackets.base import BracketBase


class DoubleEliminationBracket(BracketBase):
    def __init__(self, teams):
        super().__init__(teams)
        self.type_name = "Double Elimination"

    def generate(self):
        n = len(self.teams)
        next_pow2 = 1 if n == 0 else 2 ** math.ceil(math.log2(max(1, n)))
        seeded = self.teams[:] + [None] * (next_pow2 - n)
        first_round = []
        for i in range(0, len(seeded), 2):
            m = Match(id=str(uuid.uuid4()), round_index=0, bracket_side="main",
                      team1=seeded[i], team2=seeded[i+1])
            first_round.append(m)
        self.rounds = [first_round]
        size = len(first_round)
        while size > 1:
            next_round = [Match(id=str(uuid.uuid4()), round_index=len(self.rounds),
                                bracket_side="main", team1=None, team2=None)
                          for _ in range(size // 2)]
            self.rounds.append(next_round)
            size //= 2

    def advance(self, match: Match):
        s1, s2 = match.score
        if match.team1 and not match.team2:
            match.winner = match.team1
        elif match.team2 and not match.team1:
            match.winner = match.team2
        elif s1 > s2:
            match.winner, match.loser = match.team1, match.team2
        elif s2 > s1:
            match.winner, match.loser = match.team2, match.team1
        else:
            match.status = "Disputed"
            return
        match.status = "Completed"
        if match.round_index + 1 < len(self.rounds):
            idx = self.rounds[match.round_index].index(match)
            target = self.rounds[match.round_index + 1][idx // 2]
            if idx % 2 == 0:
                target.team1 = match.winner
            else:
                target.team2 = match.winner
        else:
            self.completed = True
            self.champion = match.winner
