def iterative_deepening_a_star ( tree, heuristic, start, goal ):
    threshold = heuristic[ start ][ goal ]
    while True:
        print( "Iteracion con umbral: " + str( threshold ) )
        distance = iterative_deepening_a_star_rec( tree, heuristic, start, goal, 0, threshold )
        if distance == float( "inf" ):
            return -1
        elif distance < 0:
            print( "Se encontro el nodo buscado" )
            return -distance
        else:
            threshold = distance


def iterative_deepening_a_star_rec ( tree, heuristic, node, goal, distance, threshold ):

    print( "Visitando nodo " + str( node ) )

    if node == goal:
        return -distance

    estimate = distance + heuristic[ node ][ goal ]
    if estimate > threshold:
        print( "Umbral con heuristica: " + str( estimate ) )
        return estimate

    min = float( "inf" )
    for i in range( len( tree[ node ] ) ):
        if tree[ node ][ i ] != 0:
            t = iterative_deepening_a_star_rec( tree, heuristic, i, goal, distance + tree[ node ][ i ], threshold )
            if t < 0:
                return t
            elif t < min:
                min = t

    return min


# graph = [
	# [ 0, 43, 64, 0, 80, 0],
	# [ 43, 0, 69, 81, 50, 0],
	# [ 64, 69, 0, 94, 0, 0 ],
	# [ 0, 81, 94, 0, 98, 157 ],
	# [ 80, 50, 0, 98, 0, 103 ],
	# [ 0, 0, 0, 157, 103, 0 ],
# ]

graph = [
            [ 1, 6, 4 ],
            [ 5, 7, 8 ],
            [ 0, 3, 2 ],
        ]

heuristic = [
            [ 1, 2, 3 ],
            [ 4, 5, 6 ],
            [ 7, 8, 0 ],
        ]
start = 0
goal = 5

print( graph, heuristic, start, goal )
