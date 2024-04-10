import subprocess
file = open("constraint-puzzles/sudoku-collection/gordon-royle-sudoku-17-entries.txt")
file = open("constraint-puzzles/kakuro-collection/games.txt")
for line in file:
    glucose_command = ["./glucose","-model","-verb=0","sudoku-cnf-gordon/"+line.split("\n")[0]]
    subprocess.call(glucose_command)
    #print(glucose_command)
