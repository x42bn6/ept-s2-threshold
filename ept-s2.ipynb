from ortools.sat.python import cp_model
import csv
import sys

def main():
    currentpoints={
            'BetBoom Team': 7500,
            'Xtreme Gaming': 6160,
            'Team Falcons': 5880,
            'Gaimin Gladiators': 5680,
            'Team Spirit': 4640,
            'Team Liquid': 3298,
            'OG': 2296,
            'G2 x iG': 1722,
            'Shopify Rebellion': 840,
            'Team Secret': 721,
            'Aurora Gaming': 660,
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
    
    def optimise(team_to_optimise):
        teamlist = list(currentpoints.keys())
        teams = len(currentpoints)
    
        def team_index(t):
            return list(currentpoints.keys()).index(t)
    
        na_qualifier = ['Shopify Rebellion', 'NA team']
        sa_qualifier = ['HEROIC', 'SA team']
        weu_qualifier = ['Team Liquid', 'OG', 'Team Secret', 'Entity', 'Tundra Esports', 'WEU team 1', 'WEU team 2']
        eeu_qualifier = ['Team Spirit', 'Virtus.pro', '1win', 'EEU team']
        mena_qualifier = ['PSG Quest', 'MENA team']
        china_qualifier = ['G2 x iG', 'LGD Gaming', 'Azure Ray', 'China team']
        sea_qualifier = ['Aurora Gaming', 'Talon Esports', 'Blacklist International', 'SEA team']
    
        r_birmingham = (6400, 4800, 4000, 3200, 2240, 2240, 1040, 1040, 560, 560, 280, 280)
        r_s23        = (6000, 5000, 4000, 3200, 2200, 2200, 1000, 1000, 500, 500, 250, 250)
        placements = 12
    
        model = cp_model.CpModel()
        x_birmingham = [[model.NewBoolVar(f'x_birmingham_{i}_{j}') for j in range(placements)] for i in range(teams)]
        x_s23        = [[model.NewBoolVar(f'x_s23_{i}_{j}') for j in range(placements)] for i in range(teams)]
        d_birmingham = [model.NewIntVar(0, 99999, f'd_birmingham_{i}') for i in range(teams)]
        d_s23        = [model.NewIntVar(0, 99999, f'd_s23_{i}') for i in range(teams)]
        d            = [model.NewIntVar(0, 99999, f'd_{i}') for i in range(teams)]
    
        # ESL One Birmingham constraints
        # Qualified teams
        birmingham_teams = ['BetBoom Team', 'Xtreme Gaming', 'Team Falcons', 'Gaimin Gladiators', 'Team Spirit', 'Team Liquid', 'G2 x iG', 'Shopify Rebellion', 'Tundra Esports', 'HEROIC', '1win', 'Talon Esports']
        for t in birmingham_teams:
            model.Add(sum(x_birmingham[team_index(t)]) == 1)
    
        # DreamLeague Season 23 constraints
        # Already-qualified teams
        for t in ['BetBoom Team', 'Xtreme Gaming', 'Team Falcons', 'Gaimin Gladiators']:
            model.Add(sum(x_s23[team_index(t)]) == 1)
    
        # Regional constraints
        # Basically, within each region, only one team can qualify and thus place
        # So if there are two qualified teams for a region, there are two rows, but only one 1 in both rows
        def add_regional_constraint(regionalqualifier, numberofqualifedteams, decisionvariable, model):
            regional_sum = 0
            for t in regionalqualifier:
                model.Add(sum(decisionvariable[team_index(t)]) <= 1)
                regional_sum += sum(decisionvariable[team_index(t)])
            model.Add(regional_sum == numberofqualifedteams)
        
        add_regional_constraint(na_qualifier, 1, x_s23, model)
        add_regional_constraint(sa_qualifier, 1, x_s23, model)
        add_regional_constraint(weu_qualifier, 2, x_s23, model)
        add_regional_constraint(eeu_qualifier, 1, x_s23, model)
        add_regional_constraint(mena_qualifier, 1, x_s23, model)
        add_regional_constraint(china_qualifier, 1, x_s23, model)
        add_regional_constraint(sea_qualifier, 1, x_s23, model)
    
        # One placement per team
        for p in range(placements):
            model.Add(sum(x_birmingham[i][p] for i in range(teams)) == 1)
            model.Add(sum(x_s23[i][p] for i in range(teams)) == 1)
        
        # Points
        for t in currentpoints:
            teamindex = team_index(t)
            d_birmingham[teamindex] = sum(x_birmingham[teamindex][p]*r_birmingham[p] for p in range(placements))
            d_s23[teamindex] = sum(x_s23[teamindex][p]*r_s23[p] for p in range(placements))
            d[teamindex] = currentpoints[teamlist[teamindex]] + d_birmingham[teamindex] + d_s23[teamindex]
    
        # Ranks
        aux = {(i, j): model.NewBoolVar(f'aux_{i}_{j}') for i in range(teams) for j in range(teams)}
        ranks = {team: model.NewIntVar(1, teams, f'ranks_{team}') for team in range(teams)}
        M = 100000
        for i in range(teams):
            for j in range(teams):
                if i == j:
                    model.Add(aux[(i, j)] == 1)
                else:
                    model.Add(d[i] - d[j] <= (1 - aux[(i, j)]) * M)
                    model.Add(d[j] - d[i] <= aux[(i, j)] * M)
            ranks[i] = sum(aux[(i, j)] for j in range(teams))

        model.Add(ranks[team_to_optimise] == 8)
        model.Maximize(d[team_to_optimise])
        solver = cp_model.CpSolver()
        status = solver.Solve(model)
        if status == cp_model.OPTIMAL:
            # Print the solution
            # Find the team ranked 8th
            for t in range(teams):
                nthplace = solver.Value(ranks[t])
                if nthplace == 8:
                    print(f"Rank 8 {teamlist[t]} had {solver.Value(d[t])} points")
            
            print("Objective value:", solver.ObjectiveValue())
            for t in range(teams):
                print(f"{teamlist[t]},{currentpoints[teamlist[t]]},{solver.Value(d_birmingham[t])},{solver.Value(d_s23[t])},{solver.Value(d[t])}")
        else:
            print("No optimal solution found.")

    # Final constraint
    for t in range(teams):
        print(f"Optimising for {list(currentpoints.keys())[t]}")
        optimise(t)
        print()

if __name__ == "__main__":
    main()
