from dataclasses import dataclass
from datetime import date

from numpy.random import uniform

from team import Team


@dataclass
class Game:
    date: date
    home_team: Team
    away_team: Team

    def simulate(self) -> "GameResult":
        while True:
            home_team_wins = uniform() <= self.home_team.current_record
            away_team_wins = uniform() <= self.away_team.current_record

            if home_team_wins and not away_team_wins:
                return GameResult(self, winner=self.home_team, loser=self.away_team)

            if away_team_wins and not home_team_wins:
                return GameResult(self, winner=self.away_team, loser=self.home_team)


@dataclass
class GameResult:
    game: Game
    winner: Team
    loser: Team
