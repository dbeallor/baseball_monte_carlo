from json import dumps
from typing import List

from team import make_teams
from schedule import ScheduleSimulationResult, make_schedule

NUM_SIMULATIONS_TO_RUN = 10000

def main():
    teams = make_teams()
    schedule = make_schedule(teams)

    results: List[ScheduleSimulationResult] = []
    for simulation_number in range(1, NUM_SIMULATIONS_TO_RUN + 1):
        print(f"Running simulation #{simulation_number}")
        results.append(schedule.simulate())
        
    division_win_rates = {}
    for team in teams:
        division_win_rates[team.name] = 0
    
    for result in results:
        division_winners = result.get_division_winners()
        for team in division_winners.values():
            division_win_rates[team] += 1
    
    for team in teams:
        division_win_rates[team.name] /= len(results)

    print(dumps(division_win_rates, indent=4))


if __name__ == "__main__":
    main()
