from ortools.sat.python import cp_model
import csv
import sys
from functools import reduce
import numpy as np
from enum import Enum
from collections import Counter

class Counter_tweaked(Counter):
    def __add__(self, other):
            if not isinstance(other, Counter):
                return NotImplemented
            result = Counter_tweaked()
            for elem, count in self.items():
                newcount = count + other[elem]
                result[elem] = newcount
            for elem, count in other.items():
                if elem not in self:
                    result[elem] = count
            return result

class Model:
    points_s21 = {
        'BetBoom Team': 1600,
        'Gaimin Gladiators': 400,
        'Team Spirit': 2400,
        'Team Liquid': 200,
        'OG': 1280,
        'Shopify Rebellion': 2000,
        'Entity': 880,
        'Tundra Esports': 880,
        'PSG Quest': 100,
        'Talon Esports': 100
    }

    points_s21_kl = {
        'OG': -384,
        'Shopify Rebellion': -2000,
        'Aurora': 100,
        'Tundra Esports': -880,
        'Entity': -264,
        'Talon Esports': -100
    }

    points_kl = {
        'BetBoom Team': 2400,
        'Team Falcons': 1680,
        'Gaimin Gladiators': 3600,
        'Team Liquid': 3000,
        'G2.iG': 1680,
        'Team Secret': 780,
        'Tundra Esports': 780,
        'Blacklist International': 420,
        'LGD Gaming': 420,
        'Azure Ray': 4800,
    }

    points_kl_s22 = {
        'Xtreme Gaming': 3360,
        'Team Secret': -234,
        'Tundra Esports': -780,
        'Azure Ray': -4800
    }

    points_s22 = {
        'BetBoom Team': 3500,
        'Xtreme Gaming': 2800,
        'Team Falcons': 4200,
        'Gaimin Gladiators': 1680,
        'Team Spirit': 2240,
        'Team Liquid': 98,
        'OG': 1400,
        'G2.iG': 42,
        'Shopify Rebellion': 840,
        'Aurora': 560,
        'Team Secret': 175,
        'Tundra Esports': 350,
        'HEROIC': 98,
        'Virtus.pro': 350,
        '1win': 42,
        'Azure Ray': 175
    }

    # Placeholder 0 EPT point teams in qualifier
    qualifier_teams = {
        #'NA team': 0,
        'nouns': 0,
        #'SA team': 0,
        'Estar_Backs': 0,
        'WEU team 1': 0,
        'WEU team 2': 0,
        #'EEU team': 0,
        'Natus Vincere': 0,
        #'MENA team': 0,
        'Nigma Galaxy': 0,
        #'China team': 0,
        'Team Zero': 0,
        #'SEA team': 0
        'Geek Fam': 0
    }
    qualifier_teams.pop('Geek Fam')
    qualifier_teams.pop('WEU team 1')
    qualifier_teams.pop('WEU team 2')
    qualifier_teams.pop('nouns')
    qualifier_teams.pop('Team Zero')
    qualifier_teams.pop('Nigma Galaxy')
    qualifier_teams.pop('Estar_Backs')

    points_s22_birmingham = {}

    points_birmingham_s23 = {}

    # Any changes after S23
    points_s23_riyadh = {}

    currentpoints = Counter_tweaked(points_s21) + Counter_tweaked(points_s21_kl) + \
        Counter_tweaked(points_kl) + Counter_tweaked(points_kl_s22) + \
        Counter_tweaked(points_s22) + Counter_tweaked(points_s22_birmingham) + \
        Counter_tweaked(points_birmingham_s23) + Counter_tweaked(points_s23_riyadh) + \
        Counter_tweaked(qualifier_teams)
    teams = len(currentpoints)
    teamlist = list(currentpoints.keys())

    na_qualifier = ['Shopify Rebellion', 'nouns']
    na_qualifier.remove('nouns')
    na_qualifier.remove('Shopify Rebellion')
    sa_qualifier = ['HEROIC', 'Estar_Backs']
    sa_qualifier.remove('HEROIC')
    sa_qualifier.remove('Estar_Backs')
    weu_qualifier = ['Team Liquid', 'OG', 'Team Secret', 'Entity', 'Tundra Esports', 'WEU team 1', 'WEU team 2']
    weu_qualifier.remove('Team Secret')
    weu_qualifier.remove('WEU team 1')
    weu_qualifier.remove('WEU team 2')
    weu_qualifier.remove('Team Liquid')
    weu_qualifier.remove('Entity')
    weu_qualifier.remove('OG')
    weu_qualifier.remove('Tundra Esports')
    eeu_qualifier = ['Team Spirit', 'Virtus.pro', '1win', 'Natus Vincere']
    eeu_qualifier.remove('Team Spirit')
    eeu_qualifier.remove('1win')
    eeu_qualifier.remove('Virtus.pro')
    mena_qualifier = ['PSG Quest', 'Nigma Galaxy']
    mena_qualifier.remove('Nigma Galaxy')
    mena_qualifier.remove('PSG Quest')
    china_qualifier = ['G2.iG', 'LGD Gaming', 'Azure Ray', 'Team Zero']
    china_qualifier.remove('LGD Gaming')
    china_qualifier.remove('G2.iG')
    china_qualifier.remove('Team Zero')
    sea_qualifier = ['Aurora', 'Talon Esports', 'Blacklist International', 'Geek Fam']
    sea_qualifier.remove('Blacklist International')
    sea_qualifier.remove('Geek Fam')
    sea_qualifier.remove('Talon Esports')
    sea_qualifier.remove('Aurora')

    r_s21        = (2400, 2000, 1600, 1280, 880,  880,  400,  400,  200, 200, 100, 100)
    r_kl         = (4800, 3600, 3000, 2400, 1680, 1680, 780,  780,  420, 420, 210, 210)
    r_s22        = (4200, 3500, 2800, 2240, 1680, 1680, 1400, 1400, 840, 560, 350, 350, 175, 175, 98, 98, 42, 42)
    r_birmingham = (6400, 4800, 4000, 3200, 2240, 2240, 1040, 1040, 560, 560, 280, 280)
    r_s23        = (6000, 5000, 4000, 3200, 2200, 2200, 1000, 1000, 500, 500, 250, 250)
    placements = 12

    birmingham_teams = ['BetBoom Team', 'Xtreme Gaming', 'Team Falcons', 'Gaimin Gladiators', 'Team Spirit', 'Team Liquid', 'G2.iG', 'Shopify Rebellion', 'Tundra Esports', 'HEROIC', '1win', 'Talon Esports']
    s23_teams = ['BetBoom Team', 'Xtreme Gaming', 'Team Falcons', 'Gaimin Gladiators', \
                 'Aurora', 'Natus Vincere', 'Shopify Rebellion', 'Team Liquid', 'Azure Ray', 'Tundra Esports', 'PSG Quest', 'HEROIC']
    
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

        def team_can_no_longer_finish(tournament, team, position):
            t = teamlist.index(team)
            model.Add(tournament[t][position] == 0)

        def team_finished(tournament, team, position):
            t = teamlist.index(team)
            model.Add(tournament[t][position] == 1)

        # Add tournament constraints here
        # param1 - x_birmingham or x_s23
        # param2 - team name, exact case, space, etc. as above
        # param3 - placement, 0-based (!!).  So 11th -> pass in 10
        # If there is a joint placement (e.g. 5th-6th), do both
        #team_can_no_longer_finish(x_birmingham, 'BetBoom Team', 10)
        #team_can_no_longer_finish(x_birmingham, 'BetBoom Team', 11)
        #team_finished(x_s23, 'Aurora', 0)
        
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

        #add_regional_constraint(self.na_qualifier, 1, x_s23, model)
        #add_regional_constraint(self.sa_qualifier, 1, x_s23, model)
        #add_regional_constraint(self.weu_qualifier, 2, x_s23, model)
        #add_regional_constraint(self.eeu_qualifier, 1, x_s23, model)
        #add_regional_constraint(self.mena_qualifier, 1, x_s23, model)
        #add_regional_constraint(self.china_qualifier, 1, x_s23, model)
        #add_regional_constraint(self.sea_qualifier, 1, x_s23, model)
    
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
            teamname = teamlist[team_to_optimise]
            maxpointsobtainable = 0
            if teamname in self.birmingham_teams:
                maxpointsobtainable += self.r_birmingham[0]
    
            if teamname in self.s23_teams:
                maxpointsobtainable += self.r_s23[0]
            elif teamname in self.na_qualifier or teamname in self.sa_qualifier or teamname in self.weu_qualifier or teamname in self.eeu_qualifier or teamname in self.mena_qualifier or teamname in self.china_qualifier or teamname in self.sea_qualifier:
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
                mat = [[0] * 11] * teams
                def format_points_tournament(points):
                    if points == None:
                        return ""
                    if points == 0:
                        return ""
                    return round(points)
                
                def format_points_in_between(points):
                    if points == None:
                        return ""
                    if points > 0:
                        return "+" + str(points)
                    return points

                for t in range(teams):
                    teamname = list(currentpoints.keys())[t]
                    
                    mat[t] = [0] * 11
                    mat[t][0] = teamname
                    mat[t][1] = format_points_tournament(self.points_s21.get(teamname))
                    mat[t][2] = format_points_in_between(self.points_s21_kl.get(teamname))
                    mat[t][3] = format_points_tournament(self.points_kl.get(teamname))
                    mat[t][4] = format_points_in_between(self.points_kl_s22.get(teamname))
                    mat[t][5] = format_points_tournament(self.points_s22.get(teamname))
                    mat[t][6] = format_points_in_between(self.points_s22_birmingham.get(teamname))
                    mat[t][7] = format_points_tournament(solver.Value(d_birmingham[t]))
                    mat[t][8] = format_points_in_between(self.points_birmingham_s23.get(teamname))
                    mat[t][9] = format_points_tournament(solver.Value(d_s23[t]))
                    mat[t][10] = solver.Value(d[t])
                sortedmatrix = sorted(mat, key=lambda x: x[10], reverse=True)

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
                print()
                print("==What does the threshold scenario look like?==")
                print(f"This is the following scenario where {{{{Team|{get_team_name(team_to_optimise)}}}}} fail to qualify with {round(objectivevalue)} points.")
                print()
                print('{| class="wikitable" style="font-size:85%; text-align: center;"')
                print("!style=\"min-width:40px\"|'''Place'''")
                print("!style=\"min-width:200px\"|'''Team'''")
                print("!style=\"min-width:50px\"|'''Point'''")
                print("|rowspan=99|")
                print("!style=\"min-width:50px\"|{{LeagueIconSmall/dreamleague|name=DreamLeague Season 21|link=DreamLeague/Season 21|date=2023-09-24}}")
                print("!style=\"min-width:50px; font-size: larger;\"|<span title=\"Point changes between DreamLeague Season 21 and ESL One Kuala Lumpur 2023\">&hArr;</span>")
                print("!style=\"min-width:50px\"|{{LeagueIconSmall/esl one|name=ESL One Kuala Lumpur 2023|link=ESL One/Kuala Lumpur/2023|date=2023-12-17}}")
                print("!style=\"min-width:50px; font-size: larger;\"|<span title=\"Point changes between ESL One Kuala Lumpur 2023 and DreamLeague Season 22\">&hArr;</span>")
                print("!style=\"min-width:50px\"|{{LeagueIconSmall/dreamleague|name=DreamLeague Season 22|link=DreamLeague/Season 22|date=2024-03-10}}")
                print("!style=\"min-width:50px; font-size: larger;\"|<span title=\"Point changes between DreamLeague Season 22 and ESL One Birmingham 2024\">&hArr;</span>")
                print("!style=\"min-width:50px\"|{{LeagueIconSmall/esl one|name=ESL One Birmingham 2024|link=ESL One/Birmingham/2024|date=2024-04-28}}")
                print("!style=\"min-width:50px; font-size: larger;\"|<span title=\"Point changes between ESL One Birmingham 2024 and DreamLeague Season 23\">&hArr;</span>")
                print("!style=\"min-width:50px\"|{{LeagueIconSmall/dreamleague|name=DreamLeague Season 23|link=DreamLeague/Season 23|date=2024-05-26}}")
                i = 0
                for row in sortedmatrix:
                    if i == 8:
                        print("|-")
                        print('| colspan="99" | Top 8 cutoff')
                    print("|-")
                    
                    teamcomponent = f"{{{{Team|{row[0]}}}}}" if not is_placeholder_team(row[0]) else f"{row[0]} with 0 EPT points"
                    s21component = f"{get_placementbg(self.r_s21, row[1])}{row[1]}"
                    klcomponent = f"{get_placementbg(self.r_kl, row[3])}{row[3]}"
                    s22component = f"{get_placementbg(self.r_s22, row[5])}{row[5]}"
                    birminghamcomponent = f"{get_placementbg(self.r_birmingham, row[7])}{row[7]}"
                    s23component = f"{get_placementbg(self.r_s23, row[9])}{row[9]}"
                    
                    print(f'| {(i+1)}')
                    print(f'!style="text-align: left;"| {teamcomponent}')
                    if i == 8:
                        print(f'| style="font-weight: bold; background-color: var(--achievement-placement-down, #cd5b5b);" | {row[10]}')
                    else:
                        print(f"| '''{row[10]}'''")
                    print(f"| {s21component}")
                    print(f"| {row[2]}")
                    print(f"| {klcomponent}")
                    print(f"| {row[4]}")
                    print(f"| {s22component}")
                    print(f"| {row[6]}")
                    print(f"| {birminghamcomponent}")
                    print(f"| {row[8]}")
                    print(f"| {s23component}")
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
    #for t in [7]:
    for t in range(len(Model().currentpoints)):
        model = Model()
        print(f"Optimising for {list(model.currentpoints.keys())[t]}")
        ninth = model.optimise(t, False, max_solution[1])
        if ninth > 0:
            old_max_solution = max_solution[1]
            if old_max_solution < ninth:
                max_solution = [t, round(max(old_max_solution, ninth))]
        print()

    model.optimise(max_solution[0], True, max_solution[1])
    
    print("Done")

if __name__ == "__main__":
    main()
