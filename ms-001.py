from random import randint

debug = False

def populate_bomb_array(bomb_array, max, bomb_count):
	while len(bomb_array) < bomb_count:
		bomb_pos = randint(0, max-1)
		if bomb_pos not in bomb_array:
			bomb_array.append(bomb_pos)

def top_left_corner(bomb_array):
    bomb_count = 0
    if bomb_array[0][1] == -1:
        bomb_count += 1
    if bomb_array[1][1] == -1:
        bomb_count += 1
    if bomb_array[1][0] == -1:
        bomb_count += 1
    return bomb_count

def top_right_corner(bomb_array):
    bomb_count = 0
    if bomb_array[0][len(bomb_array[0])-2] == -1:
        bomb_count += 1
    if bomb_array[1][len(bomb_array[0])-2] == -1:
        bomb_count += 1
    if bomb_array[1][len(bomb_array[0])-1] == -1:
        bomb_count += 1
    return bomb_count

def bottom_left_corner(bomb_array):
    bomb_count = 0
    if bomb_array[len(bomb_array)-1][1] == -1:
        bomb_count += 1
    if bomb_array[len(bomb_array)-2][1] == -1:
        bomb_count += 1
    if bomb_array[len(bomb_array)-2][0] == -1:
        bomb_count += 1
    return bomb_count

def bottom_right_corner(bomb_array):
    bomb_count = 0
    if bomb_array[len(bomb_array)-1][len(bomb_array[0])-2] == -1:
        bomb_count += 1
    if bomb_array[len(bomb_array)-2][len(bomb_array[0])-2] == -1:
        bomb_count += 1
    if bomb_array[len(bomb_array)-2][len(bomb_array[0])-1] == -1:
        bomb_count += 1
    return bomb_count

def left_edge(bomb_array, row):
    bomb_count = 0
    if bomb_array[row-1][0] == -1:
        bomb_count += 1
    if bomb_array[row-1][1] == -1:
        bomb_count += 1
    if bomb_array[row][1] == -1:
        bomb_count += 1
    if bomb_array[row+1][1] == -1:
        bomb_count += 1
    if bomb_array[row+1][0] == -1:
        bomb_count += 1
    return bomb_count

def right_edge(bomb_array, row):
    bomb_count = 0
    if bomb_array[row-1][len(bomb_array[0])-1] == -1:
        bomb_count += 1
    if bomb_array[row-1][len(bomb_array[0])-2] == -1:
        bomb_count += 1
    if bomb_array[row][len(bomb_array[0])-2] == -1:
        bomb_count += 1
    if bomb_array[row+1][len(bomb_array[0])-2] == -1:
        bomb_count += 1
    if bomb_array[row+1][len(bomb_array[0])-1] == -1:
        bomb_count += 1
    return bomb_count

def top_edge(bomb_array, column):
    bomb_count = 0
    if bomb_array[0][column-1] == -1:
        bomb_count += 1
    if bomb_array[0][column+1] == -1:
        bomb_count += 1
    if bomb_array[1][column-1] == -1:
        bomb_count += 1
    if bomb_array[1][column] == -1:
        bomb_count += 1
    if bomb_array[1][column+1] == -1:
        bomb_count += 1
    return bomb_count

def bottom_edge(bomb_array, column):
    bomb_count = 0
    if bomb_array[len(bomb_array)-1][column-1] == -1:
        bomb_count += 1
    if bomb_array[len(bomb_array)-2][column-1] == -1:
        bomb_count += 1
    if bomb_array[len(bomb_array)-2][column] == -1:
        bomb_count += 1
    if bomb_array[len(bomb_array)-2][column+1] == -1:
        bomb_count += 1
    if bomb_array[len(bomb_array)-1][column+1] == -1:
        bomb_count += 1
    return bomb_count

def test_x(row, column):
    test_x = randint(0, max-1)

def test_y(row, column):
    test_y = randint(0, max-1)

def middle_test_case(bomb_array, row, column):
    bomb_count = 0
# preceding row
    if bomb_array[row-1][column-1] == -1:
        bomb_count += 1
    if bomb_array[row-1][column] == -1:
        bomb_count += 1
    if bomb_array[row-1][column+1] == -1:
        bomb_count += 1
# same row
    if bomb_array[row][column-1] == -1:
        bomb_count += 1
    if bomb_array[row][column+1] == -1:
        bomb_count += 1
# next row
    if bomb_array[row+1][column-1] == -1:
        bomb_count += 1
    if bomb_array[row+1][column] == -1:
        bomb_count += 1
    if bomb_array[row+1][column+1] == -1:
        bomb_count += 1
    return bomb_count

def fetch_bomb_count(bomb_array, test_x, test_y):
    matrix_height = len(bomb_array)
    matrix_width = len(bomb_array[0])

    if test_x == 0:
        if test_y == 0:
            result = top_left_corner(bomb_array)
        elif test_y == matrix_width - 1:
        	result = top_right_corner(bomb_array)
        else:
        	result = top_edge(bomb_array, test_y)
    elif test_x == matrix_height - 1:
    	if test_y == 0:
    		result = bottom_left_corner(bomb_array)
    	elif test_y == matrix_width - 1:
    		result = bottom_right_corner(bomb_array)
    	else:
    		result = bottom_edge(bomb_array, test_y)
    else:
    	if test_y == 0:
    		result = left_edge(bomb_array, test_x)
    	elif test_y == matrix_width - 1:
    		result = right_edge(bomb_array, test_x)
    	else:
            result = middle_test_case(bomb_array, test_x, test_y)
    return result

def replace_bomb_count(canvas, bomb_array):
    for x in range(0, len(bomb_array)):
        for y in range(0, len(bomb_array[0])):
            if bomb_array[x][y] == 0:
                bomb_check = fetch_bomb_count(bomb_array, x, y)
                if debug:
                    print "bombs at %i, %i = %i" %(x, y, bomb_check)
                bomb_array[x][y] = bomb_check
                canvas.data.bottomLayer[x][y] = bomb_check
    if debug:
        print bomb_matrix

def create_matrix(canvas, height, width, bomb_count):
    """Create a matrix of [height][width] and mark bombs with -1."""

    max_random = height * width
    bomb_array = []
    populate_bomb_array(bomb_array, max_random, bomb_count)
    if debug:
        print bomb_array
    test_matrix = [[0 for i in xrange(width)] for i in xrange(height)]
    if debug:
        print test_matrix
    for i in range(bomb_count):
        bomb_pos = bomb_array[i-1]
        if debug:
            print bomb_pos
        test_matrix[bomb_pos/width][bomb_pos%width] = -1
        canvas.data.bottomLayer[bomb_pos/width][bomb_pos%width] = -1
    if debug:
        print test_matrix
    return test_matrix
