from random import randint

debug = False

def populate_bomb_array(bomb_array, max, bomb_count):
	while len(bomb_array) < bomb_count:
		bomb_pos = randint(0, max-1)
		if bomb_pos not in bomb_array:
			bomb_array.append(bomb_pos)
