import json, sys

from math import floor
from itertools import combinations

cells_mapping = {}
restrictions = []


def getIDDict(game):
    for key, value in cells_mapping.items():
        if game == value:
            return key
 
    return "key doesn't exist"

def getGame(key):
    if key in cells_mapping:
        return cells_mapping[key]

    return "key doesn't exist"    
 
"""
This creates all possible games for the data provided
"""

def loadKakuro(filename):
    file = open(filename).read()

    lines = [i.split('#')[0].strip() for i in file.split('\n')]
    cells = [[j.strip().replace('_','') for j in i.split('|')] 
                                        for i in lines if '|' in i]
    cols = len(cells[0])
    rows = len(cells)
    # Cada cage es un elemento que tiene en su primera coord la suma
    # y el segundo es un array con las celdas que deben cumplir dicha suma
    cages = []
    for i, line in enumerate(cells):
        for j, ijtxt in enumerate(line):
            if '\\' in ijtxt:
                dwn = ijtxt.split('\\')[0].strip()
                rgt = ijtxt.split('\\')[1].strip()

                if dwn != '':
                    cages.append([int(dwn),[]])
                    for ii in range(i+1,len(cells)):
                        if cells[ii][j].strip()=='':
                            cages[-1][-1].append((ii,j))
                        else: break

                if rgt != '':
                    cages.append([int(rgt),[]])
                    for jj in range(j+1,len(line)):
                        if cells[i][jj].strip()=='':
                            cages[-1][-1].append((i,jj))
                        else: break

    restr = createValidOptionsForEachCell(cages)
    return restr

def createValidOptionsForEachCell(celdas):
    cells = []
    # Por cada celda válida
    # Añadir restriccion de que solo puede haber un numero
    # Y al menos un numero
    for i, (num, block) in enumerate(celdas):
        for i,j in block:
            for v in range(1,10):
                cells.append((i,j,v))
            for v in range(1,10):
                for w in range(v+1,11):
                    cells.append((i,j,v))
            
    for i in range(len(cells)):
        cells_mapping[i+1] = cells[i]
    return cells


""" def createRestrictions(celdas):
    # Para cada celda no puede repetirse un numero
    for y in range(1,10):
        for z in range(1,10):
            for x in range """

""" def createGames(number_players,number_days,number_hours):
    games = []
    for i in range(0,number_players):
        for j in range(0,number_players):
            if i != j:
                for d in range(0,number_days):
                    for h in range(0,(number_hours)):
                        if i != j:
                            #print(f"{i} {j} {d} {h}")
                            games.append((i,j,d,h))
    for i in range(len(games)):
        games_mapping[i+1] = games[i]
    #print(games_mapping)
    return games """

def createDNF(restrictions,games):
    file = open("output.cnf","w")
    file.write(f"p cnf {len(games)} {len(restrictions)} \n")

    for rest in restrictions:
        file.write(f"{rest} 0\n")
    
    file.close()