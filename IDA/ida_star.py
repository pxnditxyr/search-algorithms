from copy import deepcopy

class Estate:
    def __init__ ( self, path, matrix, parent = None, g = None, h = None, f = None ):
        self.path = path        # Arriba, abajo, derecha, izquierda
        self.matrix = matrix    # Guarda el Estado (matriz completa), con el desplazamiento hecho
        self.parent = parent    # Estado del cual proviene
        self.g = g              # Función de costo
        self.h = h              # Heurística
        self.f = f              # Función de evaluación
        
    # Calcula la heurística del estado (nodo) con respecto al estado objetivo
    def heuristic_calculation ( self, matrix_objetivo ):
        self.h = 0              # Se establece la heuristica como 0
        # Para cada casilla del estado actual, si su posición es distinta a la correspondiente
        # en el estado objetivo, incrementa en 1 la heurística
        for i in range( 0, len(self.matrix) ):
            for j in range( 0, len( self.matrix[ i ] ) ):
                if self.matrix[ i ][ j ] != matrix_objetivo[ i ][ j ]:
                    self.h += 1

    # Función de evaluación
    def calcula_f(self, matrix_objetivo):
        self.heuristic_calculation(matrix_objetivo)
        self.f = self.g + self.h
    
    # Verifica si la heurística es igual a cero, entonces se habrá encontrado una solución
    def solucion(self):
        if self.h == 0:
            return True
        else:
            return False        
                
    # Calcula los futuros movimientos de la casilla en blanco, es decir, expande el nodo (estado) actual
    def expandir(self, nodo):
        lista_temporal = list()
        x, y = localiza_nodo_objetivo(self.matrix, nodo) # Guarda las coordenadas (x, y) de la casilla en blanco

        # Mueve la casilla en blanco hacia arriba
        try:
            estado_norte = deepcopy(self.matrix)                            # Hace una copia de la matriz, para calcular el nuevo movimiento
            aux = estado_norte[x][y]                                        # Hace una copia de la casilla en blanco
            if x-1 < 0:                                                     # Verifica que no exceda las filas ni las columnas de la matriz
                raise IndexError
            else:
                estado_norte[x][y] = estado_norte[x-1][y]                   # Intercambia la casilla en blanco por la casilla de arriba
                estado_norte[x-1][y] = aux                                  # Intercambia la casilla de arriba por la casilla en blanco
                lista_temporal.append(Estate("arriba", estado_norte, self)) # Guarda el estado en la lista (camino, matriz y padre)
        except IndexError:
            estado_norte = [[None]]

        # Mueve la casilla en blanco hacia abajo
        try:
            estado_sur = deepcopy(self.matrix)                           # Hace una copia de la matriz, para calcular el nuevo movimiento
            aux = estado_sur[x][y]                                       # Hace una copia de la casilla en blanco
            if x+1 > 2:                                                  # Verifica que no exceda las filas ni las columnas de la matriz
                raise IndexError
            else:
                estado_sur[x][y] = estado_sur[x+1][y]                    # Intercambia la casilla en blanco por la casilla de abajo
                estado_sur[x+1][y] = aux                                 # Intercambia la casilla de abajo por la casilla en blanco
                lista_temporal.append(Estate("abajo", estado_sur, self)) # Guarda el estado en la lista (camino, matriz y padre)
        except IndexError:
            estado_sur = [[None]]

        # Mueve la casilla en blanco hacia la izquierda
        try:
            estado_oeste = deepcopy(self.matrix)                               # Hace una copia de la matriz, para calcular el nuevo movimiento
            aux = estado_oeste[x][y]                                           # Hace una copia de la casilla en blanco
            if y-1 < 0:                                                        # Verifica que no exceda las filas ni las columnas de la matriz
                raise IndexError
            else:
                estado_oeste[x][y] = estado_oeste[x][y-1]                      # Intercambia la casilla en blanco por la casilla izquierda
                estado_oeste[x][y-1] = aux                                     # Intercambia la casilla izquierda por la casilla en blanco
                lista_temporal.append(Estate("izquierda", estado_oeste, self)) # Guarda el estado en la lista (camino, matriz y padre)
        except IndexError:
            estado_oeste = [[None]]

        # Mueve la casilla en blanco hacia la derecha
        try:
            estado_este = deepcopy(self.matrix)                             # Hace una copia de la matriz, para calcular el nuevo movimiento
            aux = estado_este[x][y]                                         # Hace una copia de la casilla en blanco
            if y+1 > 2:                                                     # Verifica que no exceda las filas ni las columnas de la matriz
                raise IndexError
            else:
                estado_este[x][y] = estado_este[x][y+1]                     # Intercambia la casilla en blanco por la casilla derecha
                estado_este[x][y+1] = aux                                   # Intercambia la casilla derecha por la casilla en blanco
                lista_temporal.append(Estate("derecha", estado_este, self)) # Guarda el estado en la lista (camino, matriz y padre)
        except IndexError:
            estado_este = [[None]]

        return lista_temporal

# Dada la casilla en blanco, se obtienen sus coordenadas (x, y) para luego calcular sus futuros movimientos
def localiza_nodo_objetivo(matrix, nodo):
    for i in range(0, len(matrix)):
        for j in range(0, len(matrix[i])):
            if matrix[i][j] == nodo:
                return i, j

def obtiene_min_f(lista):
    # Calcula el menorcosto de cada uno de los estados (nodos) expandidos
    nodo_min_f = lista[0]
    for i in lista:        
        if i.f < nodo_min_f.f:
            nodo_min_f = i
    return nodo_min_f

# Abstracción de cada una de las casillas de la matriz
class Nodo:
    def __init__(self, nodo, menores=list()):
        self.nodo = nodo       # Casilla en si
        self.menores = menores # Casillas siguientes menores
    
# Instancia cada una de las casillas y las almacena en una lista
def instanciar(matrix, lista):
    for i in matrix:
        for j in i:
            j = Nodo(j)
            lista.append(j)
            
# Convierte la matrix en un arreglo unidimensional para faciliar la búsqueda de los "menores siguientes"
def convierte_a_1d(matrix, lista):
    for i in matrix:
        for j in i:
            lista.append(j)

# Retorna las casillas siguientes menores a la casilla objetivo
def retorna_menores(nodo, matrix):
    menores = list()
    
    for i in range(matrix.index(nodo), len(matrix)):
        if matrix[i] < nodo:
            menores.append(matrix[i])
    return menores

# Calcula la distancia Manhattan entre la casilla de origen y la casilla objetivo
def calc_dist_manhattan(nodo_origen, nodo_destino, matrix):
    x_origen, y_origen = localiza_nodo_objetivo(matrix, nodo_origen)
    x_destino, y_destino = localiza_nodo_objetivo(matrix, nodo_destino)
    
    distancia = abs(x_destino - x_origen) + abs(y_destino - y_origen)
    
    return distancia

def resoluble(matrix_inicial):
    nodos = list()
    matrix_2d = list()
    sum = 0

    instanciar(matrix_inicial, nodos)         # Instancia cada una de las casillas y las almacena en una lista
    convierte_a_1d(matrix_inicial, matrix_2d) # Convierte la matriz en un arreglo unidimensional para faciliar la búsqueda de los "menores siguientes"

    for i in nodos:
        i.menores = retorna_menores(i.nodo, matrix_2d) # Retorna las casillas siguientes menores a la casilla objetivo
        sum += len(i.menores)                          # Contabiliza la cantidad de casillas menores

    # Calcula la distancia Manhattan entre la casilla de origen y la casilla objetivo
    sum += calc_dist_manhattan(9, matrix_inicial[2][2], matrix_inicial) # Y lo suma a la cantidad de menores contados

    # Si el resultado es par la matriz es resoluble
    if sum % 2 == 0:
        return True
    else:
        return False

def a_estrella(edo_inicial):
    if resoluble(edo_inicial):
        print("Matriz resoluble")

        # Inicializa las estructuras de datos
        iteracion = 0                                   # Valor de G
        nodo_en_blanco = 9                              # Nodo en blanco
        estado_inicial = Estate("inicio", mtrz_inicial) # Estado inicial
        estado_inicial.g = iteracion
        estado_inicial.calcula_f(mtrz_objetivo)         # Calcula la función de evaluación del estado inicial
        frontera = list()                               # Lista abierta
        explorado = list()                              # Lista cerrada
        explorado.append(estado_inicial)

        while True:
            nodo = explorado[-1] # Último sucesor de la lista de explorados

            # Si el nodo es la solución
            if nodo.solucion():
                # Se retrocede entre los padres de los nodos hasta construir el camino
                path = list()
                estado = nodo
                while estado.matrix != mtrz_inicial:
                    path.append(estado.path)
                    estado = estado.parent
                path.reverse()
                print("Camino encontrado: ", end=" ")
                # Imprime el camino
                for i in path:
                    print(i, end=" --> ")
                print()
                # Imprime la matrix inicial
                for i in estado_inicial.matrix:
                    print(i)
                print()
                # Imprime el nodo actual resuelto
                for i in nodo.matrix:
                    print(i)
                print("El tamaño de la solución es de {}".format(len(path)))
                print("{} estados visitados en total (frontera y explorados)".format(len(frontera)+len(explorado)))
                return

            sucesores = nodo.expandir(nodo_en_blanco) # Si no halló solución, expande los estados sucesores
            # Si algunos de los estados sucesores ya fue explorado se ignora
            remover = list()
            for i in sucesores:
                for j in explorado:
                    if i.matrix == j.matrix:
                        remover.append(i)
            
            try:
                for i in remover:
                    sucesores.remove(i)
            except ValueError:
                pass
            
            # Para cada sucesor...
            for i in sucesores:
                i.g = iteracion            # Calcula la
                i.calcula_f(mtrz_objetivo) # función de evaluación
                frontera.append(i)         # y lo añade a la frontera
            
            min_f_frontera = obtiene_min_f(frontera) # el nodo de frontera con la mínima función de costo
            explorado.append(min_f_frontera)         # pasa a la lista de explorados,
            frontera.remove(min_f_frontera)          # y se remueve de la lista de fronterizos
            
            iteracion += 1
    else:
        print("Matriz irresoluble")

# Matriz objetivo
mtrz_objetivo = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

# Matriz inicial
mtrz_inicial = [
    [2, 3, 6],
    [9, 4, 8],
    [1, 7, 5]
]

a_estrella( mtrz_inicial )

