from dataclasses import dataclass
from typing import Optional, Tuple


@dataclass
class Team:
    id: str
    name: str
    checked_in: bool = False
    wins: int = 0
    losses: int = 0
    points_for: int = 0
    points_against: int = 0


@dataclass
class Match:
    id: str
    round_index: int
    bracket_side: str
    team1: Optional[Team]
    team2: Optional[Team]
    status: str = "Scheduled"
    score: Tuple[int, int] = (0, 0)
    team1_confirmed: bool = False
    team2_confirmed: bool = False
    winner: Optional[Team] = None
    loser: Optional[Team] = None
    is_highlight: bool = False
