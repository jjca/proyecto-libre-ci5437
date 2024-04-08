import subprocess, threading, os
import datetime
import sys
import json
from utilities import createDNF, loadKakuro

def getIDDict(game):
    for key, value in games_mapping.items():
        if game == value:
            return key
 
    return "key doesn't exist"

if __name__ == '__main__':
    if len(sys.argv) < 1:
        print("Missing Argument")
        exit(1)

    celdas = loadKakuro(sys.argv[1])
    #print(celdas)
    quit()
    # Reads JSON file to transform into dictionary
    
    tournament_days = (end_date - start_date).days + 1
    tournament_hours = (datetime.datetime.combine(datetime.date.today(),end_time) - datetime.datetime.combine(datetime.date.today(),start_time)).seconds//3600
    games_per_day = (tournament_hours // 2)+1
    number_of_players = len(participants) 
    all_games = createGames(number_of_players,tournament_days,games_per_day)
    #print(all_games)
        
    restrictions = createRestrictions(tournament_days,games_per_day,number_of_players)
    createDNF(restrictions,all_games)
    variables = process_glucose()
    calendar = create_calendar(tournament_name,start_date,end_date)
    games_mapping  = {}
    for i in range(len(all_games)):
        games_mapping[i+1] = all_games[i]
    players_map = {}
    days_map = {}
    hours_map = {}
    for i in range(number_of_players):
        players_map[i] = participants[i]
    for i in range(tournament_days):
        days_map[i] = start_date + datetime.timedelta(days=i)
    for i in range(games_per_day):
        begin = datetime.datetime.combine(start_date + datetime.timedelta(days=i), start_time)
        begin += datetime.timedelta(hours=i*2)
        hours_map[i] = begin.time()


    solution_file = open("salida_glucose.txt", "r")
    solution = solution_file.readline().strip()
    solution_file.close()
    for sol in solution.split():
        if sol == "UNSAT":
            print("fail")
            break
        if int(sol) > 0:
            #print(int(sol))
            tuple = games_mapping.get(int(sol))
            #print("---------")
            #print(tuple)
            #print(f"Local {players_map[tuple[0]]} vs visitante: {players_map[tuple[1]]}")
            #print(f"El día {days_map[tuple[2]]} a las {hours_map[tuple[3]]}")
            event = add_event(players_map[tuple[0]],players_map[tuple[1]],days_map[tuple[2]],hours_map[tuple[3]])
            calendar.add_component(event)

    write_calendar(calendar)
            



    #create_calendar(variables,tournament_name,start_date,end_date,participants,start_time)