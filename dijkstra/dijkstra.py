def min_distance ( distance, queue ):
    minimum = float( "Inf" )
    min_index = -1

    for i in range ( len( distance ) ):
        if distance[ i ] < minimum and i in queue:
            minimum = distance[ i ]
            min_index = i
    return min_index


def print_path ( parent, j ):
    if parent[ j ] == -1:
        print ( j, end = " " )
        return
    print_path( parent, parent[ j ] )
    print( j, end = " " )
    
def print_solution ( distance, parent ):
    source = 0
    print( "Vertice\t\tDistancia desde el inicio\t\tCamino" )
    for i in range ( 1, len( distance ) ):
        print( f"{ source } --> { i }\t\t{ distance[ i ] }" )
        print_path( parent, i )

def dijkstra ( graph, source ):
    row = len( graph )
    column = len( graph[ 0 ] )

    distance = [ float( "Inf" ) ] * row
    parent = [ -1 ] * row

    distance[ source ] = 0
    queue = []
    for i in range ( row ):
        queue.append( i )

    while queue:
        u = min_distance( distance, queue )
        queue.remove( u )
        for i in range( column ):
            if graph[ u ][ i ] and i in queue:
                if distance[ u ] + graph[ u ][ i ] < distance[ i ]:
                    distance[ i ] = distance[ u ] + graph[ u ][ i ]
                    parent[ i ] = u
    print_solution( distance, parent )


graph = [
	[ 0, 43, 64, 0, 80, 0],
	[ 43, 0, 69, 81, 50, 0],
	[ 64, 69, 0, 94, 0, 0 ],
	[ 0, 81, 94, 0, 98, 157 ],
	[ 80, 50, 0, 98, 0, 103 ],
	[ 0, 0, 0, 157, 103, 0 ],
]

dijkstra( graph, 0 )
