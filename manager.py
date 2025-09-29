import uuid
import random
from typing import List, Optional
from models import Team, Match
from brackets.single_elim import SingleEliminationBracket
from brackets.double_elim import DoubleEliminationBracket
from brackets.round_robin import RoundRobinBracket


class TournamentManager:
    def __init__(self):
        self.teams: List[Team] = []
        self.bracket = None
        self.event_log: List[str] = []

    def log(self, msg: str):
        self.event_log.append(msg)

    def register_teams(self, names: List[str]):
        self.teams = [Team(id=str(uuid.uuid4()), name=n) for n in names]
        random.shuffle(self.teams)
        self.log(f"Registered {len(self.teams)} teams.")

    def set_bracket(self, bracket_type: str):
        if bracket_type == "Single Elimination":
            self.bracket = SingleEliminationBracket(self.teams)
        elif bracket_type == "Double Elimination":
            self.bracket = DoubleEliminationBracket(self.teams)
        elif bracket_type == "Round Robin":
            self.bracket = RoundRobinBracket(self.teams)
        self.bracket.generate()
        self.log(f"Generated {self.bracket.type_name} bracket.")

    def start_match(self, match: Match):
        if match.status == "Scheduled":
            match.status = "Ongoing"
            self.log(
                f"Match Event: {match.team1.name if match.team1 else 'BYE'} vs {match.team2.name if match.team2 else 'BYE'} started.")

    def submit_result(self, match: Match, score1: int, score2: int):
        if match.status != "Ongoing":
            self.log("Result Event: Cannot submit, match not ongoing.")
            return
        match.score = (score1, score2)
        self.log(
            f"Result Event: Submitted result {score1}-{score2} for {match.team1.name if match.team1 else 'BYE'} vs {match.team2.name if match.team2 else 'BYE'}.")

    def confirm_winner(self, match: Match, team_index: int):
        if match.status not in ("Ongoing", "Scheduled"):
            self.log("Confirm Event: Cannot confirm, match not active.")
            return
        if team_index == 1:
            match.winner, match.loser = match.team1, match.team2
        else:
            match.winner, match.loser = match.team2, match.team1
            match.status = "Completed"
            self.log(
                f"Confirm Event: {match.winner.name if match.winner else 'TBD'} confirmed as winner.")
            self.bracket.advance(match)
            if match.winner:
                match.winner.wins += 1
            if match.loser:
                match.loser.losses += 1
            if self.bracket.completed:
                self.log(
                    f"Final Event: Champion declared: {self.bracket.champion.name if self.bracket.champion else 'TBD'}.")
