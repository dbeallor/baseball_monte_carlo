from dataclasses import dataclass
from functools import lru_cache
from json import load
from pathlib import Path
from tkinter import W
from typing import List

from pandas import DataFrame
from pandas import read_csv


ROOT_PATH = Path(__file__).resolve().parent
STANDINGS_CSV_PATH = ROOT_PATH / "standings.csv"
TEAMS_JSON_PATH = ROOT_PATH / "teams.json"

@dataclass
class Team:
    name: str
    current_wins: int
    current_losses: int
    division: str
    league: str
    
    @property
    def current_record(self):
        return (
            self.current_wins 
            / (self.current_wins + self.current_losses)
        )

def load_standings_csv() -> DataFrame:
    return read_csv(STANDINGS_CSV_PATH)


def get_divisions():
    with open(TEAMS_JSON_PATH, 'r') as json_file:
        teams_data = load(json_file)

        ret = []
        for league in teams_data["leagues"]:
            for division in league["divisions"]:
                ret.append(league["name"] + " " + division["name"])

        return ret


def get_leagues():
    with open(TEAMS_JSON_PATH, 'r') as json_file:
        teams_data = load(json_file)

        ret = []
        for league in teams_data["leagues"]:
                ret.append(league["name"])

        return ret


def make_teams():
    standings_data = load_standings_csv()
    
    division_league_dict = {}
    with open(TEAMS_JSON_PATH, 'r') as json_file:
        teams_data = load(json_file)

        for league in teams_data["leagues"]:
            for division in league["divisions"]:
                for team in division["teams"]:
                    division_league_dict[team] = {}
                    division_league_dict[team]["division"] = league["name"] + " " + division["name"]
                    division_league_dict[team]["league"] = league["name"]


    teams = []
    for _, row in standings_data.iterrows():
        teams.append(
            Team(
                name=row["Tm"],
                current_wins=row["W"],
                current_losses=row["L"],
                division=division_league_dict[row["Tm"]]["division"],
                league=division_league_dict[row["Tm"]]["league"],
            )
        )

    return teams

def get_team_by_name(name: str, teams_list: List[Team]) -> Team:
    for team in teams_list:
        if team.name == name:
            return team
    
    raise ValueError(f"Invalid team name: {name}")

def get_teams_by_division(division: str, teams_list: List[Team]) -> List[Team]:
    ret = []
    for team in teams_list:
        if team.division == division:
            ret.append(team)

    return ret
