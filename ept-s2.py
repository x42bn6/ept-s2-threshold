# Inspired by this: https://tkunt.medium.com/computing-bounds-for-ranks-and-ti-qualification-of-the-dpc-2023-tour-3-870957df4ec5
# Disclaimer:
# - I'm not sure if this is correct
# - I have little experience with optimisation
# - I am not a Python developer (don't judge my code style please)
# I used OR-Tools instead of Gurobi, as I ran into license restrictions, and I'm not forking over 4 figures for it.

from ortools.sat.python import cp_model
import csv
import sys
from functools import reduce
import numpy as np
from enum import Enum

class EptSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, currentpoints, d_birmingham: list[cp_model.IntVar], d_s23: list[cp_model.IntVar], d: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__currentpoints = currentpoints
        self.__d_birmingham = d_birmingham
        self.__d_s23 = d_s23
        self.__d = d
        self.__solution_count = 0

    def on_solution_callback(self) -> None:
        self.__solution_count += 1
        teamcount = len(self.__currentpoints)
        mat = [[0] * 5] * teamcount
        for t in range(teamcount):
            mat[t] = [0] * 5
            mat[t][0] = list(self.__currentpoints.keys())[t]
            mat[t][1] = list(self.__currentpoints.values())[t]
            mat[t][2] = self.value(self.__d_birmingham[t])
            mat[t][3] = self.value(self.__d_s23[t])
            mat[t][4] = self.value(self.__d[t])
        print(np.matrix(sorted(mat, key=lambda x: x[4], reverse=True)))
        print()

    @property
    def solution_count(self) -> int:
        return self.__solution_count

class Model:
    currentpoints={
            'BetBoom Team': 7500,
            'Xtreme Gaming': 6160,
            'Team Falcons': 5880,
            'Gaimin Gladiators': 5680,
            'Team Spirit': 4640,
            'Team Liquid': 3298,
            'OG': 2296,
            'G2.iG': 1722,
            'Shopify Rebellion': 840,
            'Team Secret': 721,
            'Aurora': 660,
            'Entity': 616,
            'LGD Gaming': 420,
            'Blacklist International': 420,
            'Virtus.pro': 350,
            'Tundra Esports': 350,
            'Azure Ray': 175,
            'PSG Quest': 100,
            'HEROIC': 98,
            '1win': 42,
            
            # No points but qualified for ESL One Birmingham
            'Talon Esports': 0,
            
            # Placeholder 0 EPT point teams in qualifier
            'NA team': 0,
            'SA team': 0,
            'WEU team 1': 0,
            'WEU team 2': 0,
            'EEU team': 0,
            'MENA team': 0,
            'China team': 0,
            'SEA team': 0
        }
    teams = len(currentpoints)
    teamlist = list(currentpoints.keys())

    na_qualifier = ['Shopify Rebellion', 'NA team']
    sa_qualifier = ['HEROIC', 'SA team']
    weu_qualifier = ['Team Liquid', 'OG', 'Team Secret', 'Entity', 'Tundra Esports', 'WEU team 1', 'WEU team 2']
    eeu_qualifier = ['Team Spirit', 'Virtus.pro', '1win', 'EEU team']
    mena_qualifier = ['PSG Quest', 'MENA team']
    china_qualifier = ['G2.iG', 'LGD Gaming', 'Azure Ray', 'China team']
    sea_qualifier = ['Aurora', 'Talon Esports', 'Blacklist International', 'SEA team']

    r_birmingham = (6400, 4800, 4000, 3200, 2240, 2240, 1040, 1040, 560, 560, 280, 280)
    r_s23        = (6000, 5000, 4000, 3200, 2200, 2200, 1000, 1000, 500, 500, 250, 250)
    placements = 12

    birmingham_teams = ['BetBoom Team', 'Xtreme Gaming', 'Team Falcons', 'Gaimin Gladiators', 'Team Spirit', 'Team Liquid', 'G2.iG', 'Shopify Rebellion', 'Tundra Esports', 'HEROIC', '1win', 'Talon Esports']
    s23_teams = ['BetBoom Team', 'Xtreme Gaming', 'Team Falcons', 'Gaimin Gladiators']
    
    model = cp_model.CpModel()

    def team_index(self, t):
        return list(self.currentpoints.keys()).index(t)

    def build(self):
        model = self.model
        teams = self.teams
        teamlist = self.teamlist
        placements = self.placements
        currentpoints = self.currentpoints
        
        x_birmingham = [[model.NewBoolVar(f'x_birmingham_{i}_{j}') for j in range(placements)] for i in range(teams)]
        x_s23        = [[model.NewBoolVar(f'x_s23_{i}_{j}') for j in range(placements)] for i in range(teams)]
        d_birmingham = [model.NewIntVar(0, 99999, f'd_birmingham_{i}') for i in range(teams)]
        d_s23        = [model.NewIntVar(0, 99999, f'd_s23_{i}') for i in range(teams)]
        d            = [model.NewIntVar(0, 99999, f'd_{i}') for i in range(teams)]
        
        # ESL One Birmingham constraints
        # Qualified teams
        
        for t in self.birmingham_teams:
            model.Add(sum(x_birmingham[self.team_index(t)]) == 1)
    
        # DreamLeague Season 23 constraints
        # Already-qualified teams
        for t in self.s23_teams:
            model.Add(sum(x_s23[self.team_index(t)]) == 1)
    
        # Regional constraints
        # Basically, within each region, only one team can qualify and thus place
        # So if there are two qualified teams for a region, there are two rows, but only one 1 in both rows
        def add_regional_constraint(regionalqualifier, numberofqualifedteams, decisionvariable, model):
            regional_sum = 0
            for t in regionalqualifier:
                teamindex = self.team_index(t)
                model.Add(sum(decisionvariable[teamindex]) <= 1)
                regional_sum += sum(decisionvariable[teamindex])
            model.Add(regional_sum == numberofqualifedteams)

        add_regional_constraint(self.na_qualifier, 1, x_s23, model)
        add_regional_constraint(self.sa_qualifier, 1, x_s23, model)
        add_regional_constraint(self.weu_qualifier, 2, x_s23, model)
        add_regional_constraint(self.eeu_qualifier, 1, x_s23, model)
        add_regional_constraint(self.mena_qualifier, 1, x_s23, model)
        add_regional_constraint(self.china_qualifier, 1, x_s23, model)
        add_regional_constraint(self.sea_qualifier, 1, x_s23, model)
    
        # One placement per team
        for p in range(placements):
            model.Add(sum(x_birmingham[i][p] for i in range(teams)) == 1)
            model.Add(sum(x_s23[i][p] for i in range(teams)) == 1)
        
        # Points
        for t in self.currentpoints:
            teamindex = self.team_index(t)
            d_birmingham[teamindex] = sum(x_birmingham[teamindex][p]*self.r_birmingham[p] for p in range(placements))
            d_s23[teamindex] = sum(x_s23[teamindex][p]*self.r_s23[p] for p in range(placements))
            d[teamindex] = self.currentpoints[self.teamlist[teamindex]] + d_birmingham[teamindex] + d_s23[teamindex]

        # Ranks
        aux = {(i, j): model.NewBoolVar(f'aux_{i}_{j}') for i in range(teams) for j in range(teams)}
        ranks = {team: model.NewIntVar(1, teams, f'ranks_{team}') for team in range(teams)}
        M = 20000
        for i in range(teams):
            for j in range(teams):
                if i == j:
                    model.Add(aux[(i, j)] == 1)
                else:
                    model.Add(d[i] - d[j] <= (1 - aux[(i, j)]) * M)
                    model.Add(d[j] - d[i] <= aux[(i, j)] * M)
            ranks[i] = sum(aux[(i, j)] for j in range(teams))
        return [model, x_birmingham, x_s23, d_birmingham, d_s23, d, aux, ranks]
    
    def optimise(self, team_to_optimise, show_all, maxobjectivevalue):
        teams = self.teams
        teamlist = self.teamlist
        currentpoints = self.currentpoints
        
        [model, x_birmingham, x_s23, d_birmingham, d_s23, d, aux, ranks] = self.build()
        
        model.Add(ranks[team_to_optimise] > 8)
        model.Maximize(d[team_to_optimise])

        def flatten_array(a):
            return reduce(lambda z, y :z + y, a)
        
        # If this team can't breach the best maximum so far, don't bother
        if not show_all:
            maxpointsobtainable = 0
            if len(self.birmingham_teams) == self.placements:
                if teamlist[team_to_optimise] in self.birmingham_teams:
                    maxpointsobtainable += self.r_birmingham[0]
            else:
                maxpointsobtainable += self.r_birmingham[0]
    
            if len(self.s23_teams) == self.placements:
                if teamlist[team_to_optimise] in self.s23_teams:
                    maxpointsobtainable += self.r_s23[0]
            else:
                maxpointsobtainable += self.r_s23[0]
    
            maxpointsobtainable += self.currentpoints[self.teamlist[team_to_optimise]]
            if maxpointsobtainable < maxobjectivevalue:
                print(f"Skipping {teamlist[team_to_optimise]} as {maxpointsobtainable} < {maxobjectivevalue}")
                return -1
        
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.OPTIMAL:
            objectivevalue = solver.ObjectiveValue()
            maxobjectivevalue = max(maxobjectivevalue, objectivevalue)
            
            # Print the solution
            if (show_all):
                mat = [[0] * 5] * teams
                for t in range(teams):
                    mat[t] = [0] * 5
                    mat[t][0] = list(currentpoints.keys())[t]
                    mat[t][1] = list(currentpoints.values())[t]
                    mat[t][2] = solver.Value(d_birmingham[t])
                    mat[t][3] = solver.Value(d_s23[t])
                    mat[t][4] = solver.Value(d[t])
                sortedmatrix = sorted(mat, key=lambda x: x[4], reverse=True)

                def get_team_name(t):
                    return teamlist[t]
                
                def is_placeholder_team(teamname):
                    return teamname in ["NA team", "SA team", "WEU team 1", "WEU team 2", "EEU team", "MENA team", "China team", "SEA team"]
                
                def get_placementbg(tournamentpoints, points):
                    if points not in tournamentpoints:
                        return ""
                        
                    i = tournamentpoints.index(points)
                    if i < 4:
                        return f"{{{{PlacementBg/{i+1}}}}} "
                    return ""
                
                print("Printing Liquipedia table")
                print("==What does the threshold scenario look like?==")
                print(f"This is the following scenario where {{{{Team|{get_team_name(team_to_optimise)}}}}} fail to qualify with {int(objectivevalue)} points.")
                print()
                print('{| class="wikitable" style="font-size:85%; text-align: center;"')
                print('! Team || Initial || {{LeagueIconSmall/esl one|name=ESL One Birmingham 2024|link=ESL One/Birmingham/2024|date=2024-04-28}} || &hArr; || {{LeagueIconSmall/dreamleague|name=DreamLeague Season 23|link=DreamLeague/Season 23|date=2024-05-26}} || Total')
                i = 0
                for row in sortedmatrix:
                    if i == 8:
                        print("|-")
                        print('| colspan="99" | Top 8 cutoff')
                    print("|-")
                    teamcomponent = f"{{{{Team|{row[0]}}}}}" if not is_placeholder_team(row[0]) else f"{row[0]} with 0 EPT points"
                    birminghamcomponent = f"{get_placementbg(self.r_birmingham, row[2])}{row[2]}"
                    s23component = f"{get_placementbg(self.r_s23, row[3])}{row[3]}"
                    print(f'!style="text-align: left;"| {teamcomponent}')
                    print(f"| {row[1]}")
                    print(f"| {birminghamcomponent}")
                    print(f"|")
                    print(f"| {s23component}")
                    if i == 8:
                        print(f'| style="font-weight: bold; color: var(--achievement-placement-down, #cd5b5b);" | {row[4]}')
                    else:
                        print(f"| {row[4]}")
                    i += 1
                print("|}")
            
            print("Objective value:", objectivevalue)
            return objectivevalue
        else:
            print("No optimal solution found.")
            return -1

def main():
    # Final constraint
    max_solution = [-1, -1]
    #for t in [1]:
    for t in range(len(Model().currentpoints)):
        model = Model()
        print(f"Optimising for {list(model.currentpoints.keys())[t]}")
        ninth = model.optimise(t, False, max_solution[1])
        if ninth > 0:
            old_max_solution = max_solution[1]
            if old_max_solution < ninth:
                max_solution = [t, max(old_max_solution, ninth)]
        print()

    model.optimise(max_solution[0], True, max_solution[1])
    
    print("Done")

if __name__ == "__main__":
    main()
