import z3
import sys

def solveSudoku(file):
    str_in = open(file).read()
    lines = [i.split('#')[0].strip() for i in str_in.split('\n')]
    
    for line in lines:
        if line == "":
            break
        else: 
            X = [ [ z3.Int("x_%s_%s" % (i+1, j+1)) for j in range(9) ] 
            for i in range(9) ]
            #print(X)
            cells_c = []
            for i in range(9):
                for j in range(9):
                    cells_c.append(z3.And(1 <= X[i][j], X[i][j] <= 9))
            #cells_c = [ z3.And(1 <= X[i][j], X[i][j] <= 9) for i in range(9) for j in range(9)]
            
            rows_c = []
            for i in range(9):
                rows_c.append(z3.Distinct(X[i]))

            # Revisar xd
            cols_c = [ z3.Distinct([X[i][j] for i in range(9)]) for j in range(9)]
            
            sq_c = [ z3.Distinct( [X[3*i0+i][3*j0+j] for i in range(3) for j in range (3)])
                    for i0 in range(3) for j0 in range(3)]
            
            sudoku_c = cols_c + sq_c + rows_c + cells_c

            instance = ()
            numbers = []
            for i in range(0,len(line)):
                numbers.append(line[i])
            
            for i in range(len(numbers)):
                numbers[i] = int(numbers[i])
            for i in range(0,len(numbers),9):
                instance=instance+(tuple((numbers[i:i+9])),)
            
            instance_c = [ z3.If(instance[i][j] == 0, True, X[i][j] == instance[i][j]) 
                        for i in range(9) for j in range(9)]
            
            s = z3.Solver()
            s.add(sudoku_c + instance_c)

            if s.check() == z3.sat:
                m = s.model()
                #print(m)
                r = [ [ m.evaluate(X[i][j]) for j in range(9) ]
                        for i in range(9)]
                z3.print_matrix(r)

def solveFutoshiki(file):
    str_in = open(file).read()
    lines = []
    s = z3.Solver()
    x = 0
    cells = []
    symbols = []
    for line in str_in.split('\n'):
        if not line.strip():
            continue
        if line[0] == '|':
            for y,col in enumerate(line[1:].split('|')[:-1]):
                content = col.strip()
                c = z3.Int("x_%sy_%s" % (x, y))
                if content != '' and ('<' in content or '>' in content):
                    symbols.append(((x,y-1),content[0],(x,y)))
                    if content[1:] != '':
                        s.add(c==int(content[1:]))
                elif content != '':
                    s.add(c==int(content))
                cells.append(c)
            x +=1
        elif line[0] == '-':
            for y,col in enumerate(line[1:].split('-')[:-1]):
                content = col.strip()
                if content != '':
                    symbols.append(((x-1,y),content,(x,y)))
        
    size = x
    cells_c = []
    #Restriccion: Todos los elementos deben estar entre 1 y el tamano del tablero
    for i in cells:
        cells_c.append(z3.And(1 <= i, i <= size))

    row_res = []
    rows = []
    for i in range(size):
        curr_row = []
        for j in range(size):
            curr_row.append(cells[i * size + j])
        rows.append(curr_row)

    for row in rows:
        row_res.append(z3.Distinct(row))

    col_res = []
    cols = []
    for j in range(size):
        curr_col = []
        for i in range(size):
            curr_col.append(cells[i * size + j])
        cols.append(curr_col)

    for col in cols:
        col_res.append(z3.Distinct(col))

    for condition in symbols:
        first = cells[condition[0][0] * size + condition[0][1]]
        second = cells[condition[2][0] * size + condition[2][1]]

        if condition[1] == "<" or condition[1] == "^":
            s.add( second > first)
        elif condition[1] == ">" or condition[1] == "v":
            s.add( first > second)

    
    s.add(cells_c + row_res + col_res)
    if s.check() == z3.sat:
        m = s.model()
        #print(m)
        r = [ [ m.evaluate(cells[i * size + j]) for j in range(size) ]
                for i in range(size)]
        z3.print_matrix(r)
    else:
        print("Fail!")

def solveKakuro(file):
    str_in = open(file).read()

    lines = [i.split('#')[0].strip() for i in str_in.split('\n')]
    cells = [[j.strip().replace('_','') for j in i.split('|')] 
                                        for i in lines if '|' in i]
    cols = len(cells[0])
    rows = len(cells)
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
    blank_cells = {}
    for i, (num,block) in enumerate(cages):
        for i,j in block:
            blank_cells[i,j] = z3.Int("x_%s_%s"%(i,j))
    cells_c = []
    for i, (num,block) in enumerate(cages):
        for i,j in block:
            cells_c.append(z3.And(1 <= blank_cells[i,j], blank_cells[i,j] <= 9))
    all_different = []

    all_different = [ z3.Distinct([blank_cells[i,j] for i,j in block]) for i, (num,block) in enumerate(cages)]


    #cols_c = [ z3.Distinct([X[i][j] for i in range(9)]) for j in range(9)]
    f = z3.Function('f',z3.IntSort())
    x = z3.Int('x')
    sums_c = []
        #pycode = ("solver.Add(" + " + ".join("cells[%d,%d]"%(i,j) for i,j in block) + " == %d) "%num)
        
        #sums_c = [z3.ForAll([x],(blank_cells[i,j] for i,j in block) == num)]
    sums_c = [z3.ForAll([x],z3.Sum([blank_cells[i,j] for i,j in block]) == num) for k, (num,block) in enumerate(cages)]

    #for i, (num,block) in enumerate(cages):
     #   for i,j in block:
      #      print(blank_cells[i,j])
    #sums_c = [ z3.Sum( [blank_cells[i,j] for i, (num,block) in enumerate(cages) for i,j in block])]

    # [ z3.Distinct([X[i][j] for i in range(9)]) for j in range(9)]
    #print(blank_cells)
    #print(all_different)
    #print(cells_c)
    
    """ X = [ [ z3.Int("x_%s_%s" % (i+1, j+1)) for j in range(9) ] 
      for i in range(9) ]
    #print(X)
    cells_c = []
    for i in range(9):
        for j in range(9):
            cells_c.append(z3.And(1 <= X[i][j], X[i][j] <= 9))
    #cells_c = [ z3.And(1 <= X[i][j], X[i][j] <= 9) for i in range(9) for j in range(9)]
    
    rows_c = []
    for i in range(9):
        rows_c.append(z3.Distinct(X[i]))

    # Revisar xd
    cols_c = [ z3.Distinct([X[i][j] for i in range(9)]) for j in range(9)]
    
    #print(cols_c)

    sq_c = [ z3.Distinct( [X[3*i0+i][3*j0+j] for i in range(3) for j in range (3)])
            for i0 in range(3) for j0 in range(3)] """
    kakuro_c = sums_c + all_different + cells_c

    """ str_in = open(file).read()
    instance = ()
    numbers = []
    for i in range(0,len(str_in)):
        numbers.append(str_in[i])
        #instance = instance + temp
    #print(numbers)
    for i in range(len(numbers)):
        numbers[i] = int(numbers[i])
    for i in range(0,len(numbers),9):
        instance=instance+(tuple((numbers[i:i+9])),) """
        
    """ print(instance) """

    #instance = ((','.join(str_in[i:i+9])+) for i in range(0,len(str_in),9))

    
    #instance_c = [ z3.If(blank_cells[i][j] == 0, True, blank_cells[i][j] == blank_cells[i][j]) 
    #            for i in range(9) for j in range(9)]
    
    #print(instance_c)

    s = z3.Solver()
    #print(s)
    blank_cells_l = [blank_cells[i,j] for i,j in blank_cells]
    #print(blank_cells_l)
    s.add(kakuro_c)
    #print(s.dimacs())
    #s.push()
    #s.add(instance_c)
    
    if s.check() == z3.sat:
        m = s.model()

        r = [ [m.evaluate(blank_cells[i,j]) for i,j in block]
               for i, (num,block) in enumerate(cages)]
        z3.print_matrix(r)
    

    #for i in range(0,len(r),24):
    #    print(r[i:24+i])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Missing Argument")
        exit(1)
        
    print("Hola, se usara el solver Z3")
    if sys.argv[1] == "-s":
        solveSudoku(sys.argv[2])
    elif sys.argv[1] == "-k":
        solveKakuro(sys.argv[2])
    elif sys.argv[1] == "-f":
        solveFutoshiki(sys.argv[2])




