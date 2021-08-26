## Funciones para imprimir
def print_path ( parent, j ):                       # Imprimir el camino recibe una lista de indices de nodo considerado padre en ese momento para ver si tiene mas hijos, y el indice j
    if parent[ j ] == -1:                           # En la lista de indices nodos padre, se busca en el indice j si es -1 para verificar si es un nodo hoja o no tiene conexion
        print ( j, end = " -> " )                   # Imprime j y termina con -> siempre dado que es el primer nodo
        return                                      # Retorna para no seguir si es el nodo hoja o si no tiene mas conexiones
    print_path( parent, parent[ j ] )               # Se llama recursivamente pero esta vez se envia el valor de otro indice que esta en la lista parent
    print( j, end = " -> " )                        # Se imprime j y -> para finalizar
    
def print_solution ( distance, parent ):            # Imprime toda la solucion anclando el camino
    source = 0                                      # El nodo de inicio sera 0
    print( "Vertice\t\tDistancia desde el inicio\t\tCamino" ) # Los nombres de la tabla, \t indica que es un tabulado
    for i in range ( 1, len( distance ) ):          # for desde 1 a la longitud de la distancia
        print( f"{ source } --> { i }\t\t{ distance[ i ] }", end = "\t\t\t\t\t" ) # Se hace un print de un F string, el cual nos ayuda a hacer un format directo o su equivalente ( "hola {0}".format( 1 ) )
                                                                                  # Su equivalente en c++ cout << "hola" << 1 << endl;
        print_path( parent, i )                     # Se llama a la funcion imprime camino con la lista de indices de nodos
        print( "" )                                 # Dado que se tiene un end con \t necesitamos hacer un salto de linea por esto un print con una cadena vacia


## Funcion de distancia minima
def min_distance ( distance, queue ):               # Esta funcion recibe la distancia y la estructura cola que contendra los nodos del grafo
    minimum = float( "Inf" )                        # Se necesita establecer un minimo el cual sera infinito, entonces comparariamos por ejemplo 1000 < Inf, y ahora el minimo seria 1000 si hay menores se los encontrara y cambiara de igual forma
    min_index = -1                                  # Dado que no existe un indice -1, cuando se halle un minimo se cambiara con el indice del minimo

    for i in range ( len( distance ) ):             # Se hace un for desde 0 hasta la longitud de las distancias
        if distance[ i ] < minimum and i in queue:  # Se verifica que las distancias en i sean menores al minimo actual para hacer el cambio, y tambien se verifica que el indice este en la estructura cola
            minimum = distance[ i ]                 # Se realiza el cambio de las distancias
            min_index = i                           # Se realiza el cambio de los indices
    return min_index                                # Se retorna el indice de la distancia minima




def dijkstra ( graph, source ):                     # Algoritmo de dijkstra recibe el grafo y el nodo de inicio
    row = len( graph )                              # Se establece una variable que contiene el numero de filas del grafo
    column = len( graph[ 0 ] )                      # Se establece una variable que contiene el numero de columnas del grafo

    distance = [ float( "Inf" ) ] * row             # Se establece una lista con la razon que simboliza el infinito, la lista del tamaño de las filas
    parent = [ -1 ] * row                           # Asi mismo una lista con indices -1

    distance[ source ] = 0                          # Se establece la distancia del origen como 0
    queue = []                                      # Una lista que represetara la estructura cola
    for i in range ( row ):                         # Un for desde 0 hasta el numero de filas del grafo
        queue.append( i )                           # Y se va añadiendo i en la estructura cola

    while queue:                                    # Mientras la estructura cola siga teniendo datos, dado que tenemos que sacar los nodos ya recorridos
        u = min_distance( distance, queue )         # u guardara la distancia minima
        queue.remove( u )                           # Y se removera de la estructura cola, el elemento u es decir aquel con la distancia minima
        for i in range( column ):                   # For desde 0 hasta el numero de columnas 
            if graph[ u ][ i ] and i in queue:      # Si el grafo en u ( distancia minima ) e i el indice recorrido sea diferente de 0 ya que 0 representa false e i este en la estructura cola
                if distance[ u ] + graph[ u ][ i ] < distance[ i ]: # Si la distancia en u + el grafo en la distancia minima e i son menores a la distancia en i, para comprobar cual es menor si la actual o la que estamos encontrando
                    distance[ i ] = distance[ u ] + graph[ u ][ i ] # Entonces se hace el cambio en la lista de distancias
                    parent[ i ] = u                                 # Y la lista de indices
    print_solution( distance, parent )              # Y se imprime la solucion con estos datos


## Se crea el grafo de el departamento asignado
graph = [
	[ 0, 43, 64, 0, 80, 0],
	[ 43, 0, 69, 81, 50, 0],
	[ 64, 69, 0, 94, 0, 0 ],
	[ 0, 81, 94, 0, 98, 157 ],
	[ 80, 50, 0, 98, 0, 103 ],
	[ 0, 0, 0, 157, 103, 0 ],
]

## Se llama a la funcion dijsktra con el grafo y el nodo origen deseado para comenzar el proceso
dijkstra( graph, 0 )
