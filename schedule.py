from __future__ import division
from dataclasses import dataclass
from datetime import date
from json import load
from pathlib import Path
from typing import Dict
from typing import List

from game import Game, GameResult
from team import Team, get_divisions, get_teams_by_division
from team import get_team_by_name

ROOT_PATH = Path(__file__).resolve().parent
SCHEDULE_JSON_PATH = ROOT_PATH / "schedule.json"


@dataclass
class Schedule:
    teams: List[Team]
    dates: List[date]
    games: List[Game]

    def simulate(self) -> "ScheduleSimulationResult":
        results = []
        for game in self.games:
            results.append(game.simulate())

        return ScheduleSimulationResult(self, results=results)


@dataclass
class ScheduleSimulationResult:
    schedule: Schedule
    results: List[GameResult]

    def get_team_final_record(self, team: Team) -> float:
        simulation_wins = 0
        simulation_losses = 0

        for result in self.results:
            if result.winner == team:
                simulation_wins += 1
            if result.loser == team:
                simulation_losses += 1

        total_wins = team.current_wins + simulation_wins
        total_loses = team.current_losses + simulation_losses

        return total_wins / (total_wins + total_loses)


    def get_division_winner(self, divsion: str) -> Team:
        teams = get_teams_by_division(divsion, self.schedule.teams)

        records = {}
        for team in teams:
            records[team.name] = self.get_team_final_record(team)

        return max(records, key=records.get)


    def get_division_winners(self) -> Dict[str, Team]:
        return {
            division: self.get_division_winner(division)
            for division in get_divisions()
        }

def make_schedule(teams_list: List[Team]) -> Schedule:
    dates = []
    games = []

    with open(SCHEDULE_JSON_PATH, 'r') as json_file:
        schedule_data = load(json_file)

        for date_data in schedule_data["dates"]:
            dates.append(date_data["date"])

            for game_data in date_data["games"]:
                if game_data["gameType"] == "R":
                    games.append(
                        Game(
                            date=date_data["date"],
                            home_team=get_team_by_name(
                                name=game_data["teams"]["home"]["team"]["name"], 
                                teams_list=teams_list,
                            ),
                            away_team=get_team_by_name(
                                name=game_data["teams"]["away"]["team"]["name"], 
                                teams_list=teams_list,
                            ),
                        )
                    )

    return Schedule(teams_list, dates, games)
