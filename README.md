# Proyecto Libre de la materia CI5437

Elaborado por:
Yerimar Manzo - 14-10611
Jorge Correia -14-10254

# Objetivo

El presente proyecto tiene como objetivo modelar en SAT el juego kakuro para verificar si la solución dada por el solver es válida.

# Cómo ejecutar

Para ejecutar el proyecto, debe usarse Python con las librería `z3`. Puede usarse `pip install -r requirements.txt` para instalar las depedencias del proyecto.

## Resolver Kakuro

El formato de lectura y los casos de prueba son los que se usan en el proyecto https://github.com/heetbeet/constraint-puzzles.

Cada archivo tiene un tablero de Kakuro en blanco, y el formato del tablero es el siguiente:

- Cada línea puede tener distintos caracteres:
  - El caracter es `.` representa una celda negra.
  - La `|` representa una separación de columna
  - Una celda `X\Y` donde X e Y son números o _ representa una celda de pistas. No pueden habes celdas `_\_`
  - Las líneas horizontales se separan con `---+----`. 
  - Las celdas con espacios en blanco son celdas válidas para introducir valores.

## Ejemplo de ejecución

```python3 main.py -k constraint-puzzles/kakuro-collection/kakuro-grandgames.net-23104.txt```

## Resolver Sudoku

El caso del Sudoku es equivalente al de Kakuro.

El formato de lectura también es el mismo del proyecto https://github.com/heetbeet/constraint-puzzles.

Para los archivos de prueba de Sudoku, cada línea es un tablero, de forma que cada línea es un string de números entre 0 y 9 de longitud 81.

El número 0 representa un espacio en blanco, mientras que los números 1 al 9 representan valores de pista ya indicados al inicio.

## Ejemplo de ejecución

 ```python3 main.py -s constraint-puzzles/sudoku-collection/gordon-royle-sudoku-17-entries.txt```

## Resolver Futoshiki

En el caso de Futoshiki, se creo un formato de lectura.

Las lineas que contienen "|" son filas de casillas; y aquellas con "-" son los espacios entre las filas.

Cada linea debe llenarse con valores de 1 al numero de columnas, sin repeticion. Aquellos que ya estan dispuestos al inicio, son valores de pista y aquellos
espacios vacios entre "|  |", deben llenarse.

Los simbolos "<",">" indican que se deben comparar los valores de los numeros en casillas adyacentes horizontalmente. Los simbolos "^" y "v" indican que
se deben comparar los valores de los numeros adyacentes verticalmente.

## Ejemplo de ejecución

 ```python3 main.py -f constraint-puzzles/futoshiki-collection/futoshiki-1.txt```


## Glucose y CNF

El Z3 Solver permite exportar las restricciones a un archivo DIMACS CNF. Este se genera usando el método `.dimacs` de la clase `Solver`. Actualmente ese código está comentado.

Para ejecutar Glucose se usó un script, el cual lee la lista de archivos CNF creados para luego evaluarlos.