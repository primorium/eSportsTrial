import uuid
from models import Team, Match
from brackets.base import BracketBase


class RoundRobinBracket(BracketBase):
    def __init__(self, teams):
        super().__init__(teams)
        self.type_name = "Round Robin"

    def generate(self):
        teams = self.teams[:]
        if len(teams) % 2 == 1:
            teams.append(None)
        n = len(teams)
        rotation = teams[1:]
        rounds = []
        for r in range(n - 1):
            pairings = []
            left = [teams[0]] + rotation[: (n // 2) - 1]
            right = rotation[(n // 2) - 1:][::-1]
            for t1, t2 in zip(left, right):
                pairings.append(Match(id=str(uuid.uuid4()), round_index=r,
                                      bracket_side="rr", team1=t1, team2=t2))
            rounds.append(pairings)
            rotation = rotation[1:] + rotation[:1]
        self.rounds = rounds

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
