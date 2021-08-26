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
    def heuristic_calculation ( self, target_matrix ):
        self.h = 0              # Se establece la heuristica como 0
        # Para cada casilla del estado actual, si su posición es distinta a la correspondiente
        # en el estado objetivo, incrementa en 1 la heurística
        for i in range( 0, len( self.matrix ) ):
            for j in range( 0, len( self.matrix[ i ] ) ):
                if self.matrix[ i ][ j ] != target_matrix[ i ][ j ]:
                    self.h += 1

    # Función de evaluación
    def calcula_f( self, target_matrix ):
        self.heuristic_calculation( target_matrix )
        self.f = self.g + self.h
    
    # Verifica si la heurística es igual a cero, entonces se habrá encontrado una solución
    def solucion( self ):
        if self.h == 0:
            return True
        else:
            return False        
                
    # Calcula los futuros movimientos de la casilla en blanco, es decir, expande el nodo (estado) actual
    def expandir( self, node ):
        temporal_list = list()
        x, y = locate_target_node( self.matrix, node )                          # Guarda las coordenadas (x, y) de la casilla en blanco
        # Mueve la casilla en blanco hacia arriba
        try:
            northern_state = deepcopy( self.matrix )                            # Hace una copia de la matriz, para calcular el nuevo movimiento
            aux = northern_state[ x ][ y ]                                      # Hace una copia de la casilla en blanco
            if x - 1 < 0:                                                       # Verifica que no exceda las filas ni las columnas de la matriz
                raise IndexError
            else:
                northern_state[ x ][ y ] = northern_state[ x - 1 ][ y ]         # Intercambia la casilla en blanco por la casilla de arriba
                northern_state[ x - 1 ][ y ] = aux                              # Intercambia la casilla de arriba por la casilla en blanco
                temporal_list.append( Estate("arriba", northern_state, self) )  # Guarda el estado en la lista (camino, matriz y padre)
        except IndexError:
            northern_state = [[ None ]]

        # Mueve la casilla en blanco hacia abajo
        try:
            southern_state = deepcopy( self.matrix )                                    # Hace una copia de la matriz, para calcular el nuevo movimiento
            aux = southern_state[ x ][ y ]                                              # Hace una copia de la casilla en blanco
            if x+1 > 2:                                                                 # Verifica que no exceda las filas ni las columnas de la matriz
                raise IndexError
            else:
                southern_state[ x ][ y ] = southern_state[ x + 1 ][ y ]                 # Intercambia la casilla en blanco por la casilla de abajo
                southern_state[ x + 1 ][ y ] = aux                                      # Intercambia la casilla de abajo por la casilla en blanco
                temporal_list.append( Estate( "abajo", southern_state, self ) )         # Guarda el estado en la lista (camino, matriz y padre)
        except IndexError:
            southern_state = [[ None ]]

        # Mueve la casilla en blanco hacia la izquierda
        try:
            western_state = deepcopy( self.matrix )                                     # Hace una copia de la matriz, para calcular el nuevo movimiento
            aux = western_state[ x ][ y ]                                                   # Hace una copia de la casilla en blanco
            if y-1 < 0:                                                                 # Verifica que no exceda las filas ni las columnas de la matriz
                raise IndexError
            else:
                western_state[ x ][ y ] = western_state[ x ][ y - 1 ]                   # Intercambia la casilla en blanco por la casilla izquierda
                western_state[ x ][ y - 1 ] = aux                                       # Intercambia la casilla izquierda por la casilla en blanco
                temporal_list.append( Estate( "izquierda", western_state, self ) )      # Guarda el estado en la lista (camino, matriz y padre)
        except IndexError:
            western_state = [[ None ]]

        # Mueve la casilla en blanco hacia la derecha
        try:
            eastern_state = deepcopy( self.matrix )                                     # Hace una copia de la matriz, para calcular el nuevo movimiento
            aux = eastern_state[ x ][ y ]                                               # Hace una copia de la casilla en blanco
            if y + 1 > 2:                                                               # Verifica que no exceda las filas ni las columnas de la matriz
                raise IndexError
            else:
                eastern_state[ x ][ y ] = eastern_state[ x ][ y + 1 ]                   # Intercambia la casilla en blanco por la casilla derecha
                eastern_state[ x ][ y + 1 ] = aux                                       # Intercambia la casilla derecha por la casilla en blanco
                temporal_list.append( Estate( "derecha", eastern_state, self ) )        # Guarda el estado en la lista (camino, matriz y padre)
        except IndexError:
            eastern_state = [[ None ]]
        return temporal_list

# Dada la casilla en blanco, se obtienen sus coordenadas (x, y) para luego calcular sus futuros movimientos
def locate_target_node( matrix, node ):
    for i in range( 0, len( matrix ) ):
        for j in range( 0, len( matrix[ i ] ) ):
            if matrix[ i ][ j ] == node:
                return i, j

def get_min_f( my_list ):
    # Calcula el menor costo de cada uno de los estados (nodos) expandidos
    node_min_f = my_list[ 0 ]
    for i in my_list:        
        if i.f < node_min_f.f:
            node_min_f = i
    return node_min_f

# Abstracción de cada una de las casillas de la matriz
class node:
    def __init__( self, node, minor = list() ):
        self.node = node                            # Casilla en si
        self.minor = minor                          # Casillas siguientes menores
    
# Instancia cada una de las casillas y las almacena en una lista
def instantiate( matrix, my_list ):
    for i in matrix:
        for j in i:
            j = node( j )
            my_list.append( j )
            
# Convierte la matrix en un arreglo unidimensional para faciliar la búsqueda de los "menores siguientes"
def convierte_a_1d( matrix, my_list ):
    for i in matrix:
        for j in i:
            my_list.append( j )

# Retorna las casillas siguientes menores a la casilla objetivo
def retorna_minor( node, matrix ):
    minor = list()
    
    for i in range( matrix.index( node ), len( matrix ) ):
        if matrix[i] < node:
            minor.append(matrix[i])
    return minor

# Calcula la distancia Manhattan entre la casilla de origen y la casilla objetivo
def calc_dist_manhattan( source_node, destination_node, matrix ):
    x_source, y_source = locate_target_node( matrix, source_node )
    x_destination, y_destination = locate_target_node( matrix, destination_node )
    
    distance = abs(x_destination - x_source) + abs(y_destination - y_source)
    
    return distance

def resoluble(matrix_inicial):
    nodes = list()
    matrix_2d = list()
    sum = 0

    instantiate( matrix_inicial, nodes )                        # Instancia cada una de las casillas y las almacena en una lista
    convierte_a_1d( matrix_inicial, matrix_2d )                 # Convierte la matriz en un arreglo unidimensional para faciliar la búsqueda de los "menores siguientes"

    for i in nodes:
        i.minor = retorna_minor( i.node, matrix_2d )            # Retorna las casillas siguientes menores a la casilla objetivo
        sum += len( i.minor )                                   # Contabiliza la cantidad de casillas menores

    # Calcula la distancia Manhattan entre la casilla de origen y la casilla objetivo
    sum += calc_dist_manhattan( 9, matrix_inicial[ 2 ][ 2 ], matrix_inicial ) # Y lo suma a la cantidad de menores contados
    # Si el resultado es par la matriz es resoluble
    if sum % 2 == 0:
        return True
    else:
        return False

def ida_star( initial_state ):

    if resoluble( initial_state ):
        print("Matriz resoluble")

        # Inicializa las estructuras de datos
        iteration = 0                                       # Valor de G
        white_square = 9                                    # Nodo en blanco
        estado_inicial = Estate( "inicio", initial_matrix )   # Estado inicial
        estado_inicial.g = iteration
        estado_inicial.calcula_f( target_matrix )           # Calcula la función de evaluación del estado inicial
        frontera = list()                                   # Lista abierta
        explorado = list()                                  # Lista cerrada
        explorado.append( estado_inicial )

        while True:
            node = explorado[ -1 ] # Último sucesor de la lista de explorados

            # Si el nodo es la solución
            if node.solucion():
                # Se retrocede entre los padres de los nodos hasta construir el camino
                path = list()
                estado = node
                while estado.matrix != initial_matrix:
                    path.append(estado.path)
                    estado = estado.parent
                path.reverse()
                print("Camino encontrado: ", end=" ")
                # Imprime el camino
                for i in path:
                    print( i, end=" => " )
                print()
                # Imprime la matrix inicial
                for i in estado_inicial.matrix:
                    print( i )
                print()
                # Imprime el nodo actual resuelto
                for i in node.matrix:
                    print( i )
                print( f"El tamaño de la solución es de { len(path) }" )
                print("{} estados visitados en total (frontera y explorados)".format( len( frontera ) + len( explorado ) ))
                return

            sucesores = node.expandir(white_square) # Si no halló solución, expande los estados sucesores
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
            
            for i in sucesores:
                i.g = iteration                         # Calcula la
                i.calcula_f( target_matrix )            # función de evaluación
                frontera.append(i)                      # y lo añade a la frontera
            
            min_f_frontera = get_min_f( frontera )      # el nodo de frontera con la mínima función de costo
            explorado.append( min_f_frontera )          # pasa a la lista de explorados,
            frontera.remove( min_f_frontera )           # y se remueve de la lista de fronterizos

            iteration += 1
    else:
        print("Matriz irresoluble")

# Matriz objetivo
target_matrix = [
    [ 1, 2, 3 ],
    [ 4, 5, 6 ],
    [ 7, 8, 9 ]
]

# Matriz inicial
initial_matrix = [
    [ 2, 3, 6 ],
    [ 9, 4, 8 ],
    [ 1, 7, 5 ]
]

ida_star( initial_matrix )

