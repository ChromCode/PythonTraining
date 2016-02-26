from random import randint

debug = False

def populate_bomb_array(bomb_array, max, bomb_count):
	while len(bomb_array) < bomb_count:
		bomb_pos = randint(0, max-1)
		if bomb_pos not in bomb_array:
			bomb_array.append(bomb_pos)

def test_x(row, column):
    test_x = randint(0, max-1)

def test_y(row, column):
    test_y = randint(0, max-1)

def fetch_bomb_count(bomb_array, test_x, test_y):
    x_range = [ test_x-1, test_x, test_x+1 ] 
    y_range = [ test_y-1, test_y, test_y+1 ]
    bomb_count = 0
    for x in x_range:
        for y in y_range:
            try:
                if bomb_array[x][y] == -1:
                    bomb_count += 1
            except IndexError:
                if debug: print "IndexErroc, do nothing"
    return bomb_count

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
