from ortools.constraint_solver import pywrapcp
from itertools import product
from misc import timeme

def display_solution(cells):
    for i, line in enumerate(cells):
        for j, c in enumerate(line):
            print(c.Value(),end=' ')
            if (j+1)%3==0 and (j+1)!=9:
                print('|', end=' ')
        if (i+1)%3==0 and (i+1)!=9:
            print('\n------+-------+------')
        else:
            print()
    
def verify_solution(cells):
    #rows and cols
    for i in range(9):
        if len(set(cells[i][j].Value() for j in range(9)))!=9:
            return False
        if len(set(cells[j][i].Value() for j in range(9)))!=9:
            return False
    
    #blocks
    for i in range(0,9,3):
        for j in range(0,9,3):
            if len(set(cells[i+ii][j+jj].Value() 
                       for ii in range(3) for jj in range(3)))!=9:
                return False
            
    return True

def cells_from_txt(txt):
    #strip comments
    txt = '\n'.join(i.split('#')[0] for i in txt.split('\n')) 
    cells = []
    idx=0
    txt = txt.replace('.','0') 
    for i in txt:
        if i in '01234567890':
            if idx%9==0:
                cells.append([])
            idx+=1
            cells[-1].append(int(i))
        if idx/9 ==9: break
    return cells

def sudoku(sudoku_cells):
    with timeme("Setup time:"):
        N = 9
        solver = pywrapcp.Solver(__file__)

        cells = []
        for i in range(N):
            cells.append([])
            for j in range(N):
                if sudoku_cells[i][j] == 0:
                    cells[-1].append(solver.IntVar(1,9,'x(%d,%d)'%(i,j)))
                else:
                    #reduce the domain to a single entry -- i.e. observe the cell
                    cells[-1].append(solver.IntVar(sudoku_cells[i][j],
                                                   sudoku_cells[i][j],
                                                   'x(%d,%d)'%(i,j)))

        #rows and cols
        for i in range(N):
            solver.Add(solver.AllDifferent(cells[i]))
            solver.Add(solver.AllDifferent([cells[j][i] for j in range(N)]))

        #blocks
        for i in range(0,9,3):
            for j in range(0,9,3):
                solver.Add(solver.AllDifferent([cells[i+ii][j+jj] 
                                     for ii in range(3) for jj in range(3)]))

        cells_flat = []
        for i in range(N):
            for j in range(N):
                cells_flat.append(cells[i][j])

        db= solver.Phase(
                cells_flat,
                solver.CHOOSE_MIN_SIZE_LOWEST_MAX,
                solver.ASSIGN_CENTER_VALUE
            )
        solver.NewSearch(db)
        
    with timeme("Solver time:"):
        while solver.NextSolution():
            yield cells

if __name__ == "__main__":
    import sys
    if len(sys.argv)>=2:
        sudoku_txts = [open(sys.argv[1]).read()]
    else: 
        sudoku_txts = [line for line in open('sudoku-collection/gordon-royle-sudoku-17-entries.txt').read().split('\n')
                       ]
    for txt in sudoku_txts:
        if len(sudoku_txts)>1:
            print('\n'+txt)
        for solution in sudoku((cells_from_txt(txt))):
            display_solution(solution)