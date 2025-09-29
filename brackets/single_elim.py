import uuid
import math
from models import Team, Match
from brackets.base import BracketBase


class SingleEliminationBracket(BracketBase):
    def __init__(self, teams):
        super().__init__(teams)
        self.type_name = "Single Elimination"
        self.losers_rounds = []
        self.grand_final = None

    def generate(self):
        n = len(self.teams)
        next_pow2 = 1 if n == 0 else 2 ** math.ceil(math.log2(max(1, n)))
        seeded = self.teams[:] + [None] * (next_pow2 - n)
        first_round = [Match(id=str(uuid.uuid4()), round_index=0, bracket_side="main",
                             team1=seeded[i], team2=seeded[i+1])
                       for i in range(0, len(seeded), 2)]
        self.rounds = [first_round]
        self.grand_final = Match(id=str(uuid.uuid4()), round_index=0,
                                 bracket_side="grand_final", team1=None, team2=None)

    def advance(self, match: Match):
        s1, s2 = match.score
        if s1 > s2:
            match.winner, match.loser = match.team1, match.team2
        elif s2 > s1:
            match.winner, match.loser = match.team2, match.team1
        else:
            match.status = "Disputed"
            return
        match.status = "Completed"
        if match.bracket_side == "grand_final":
            self.completed = True
            self.champion = match.winner
