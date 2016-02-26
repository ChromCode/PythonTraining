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
                if debug: print "IndexError, do nothing"
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

# Start of the GUI Code from the GUI branch
#used to run the timer display in the main game at a constant speed
def scoreTime(canvas):
    delay = canvas.data.delay
    canvas.data.time += 1
    if canvas.data.gameOver == False:
        #checks for victory every second
        checkMines(canvas)
        redrawAll(canvas)
    def f(): scoreTime(canvas)
    canvas.after(delay, f) # pause, then call timerFired again

#left-click
def mousePressed1(event,canvas):
    if(event.y >= 0 and event.y <= canvas.data.scoreBox):
        pass
    #the grid of the game excludes the score box at the top
    row = (event.y - canvas.data.scoreBox)/canvas.data.cellSize
    col = (event.x)/canvas.data.cellSize
    #get bounds for the restart button
    smileyLeft = canvas.data.width/2 - canvas.data.scoreBox /2 
    smileyRight = canvas.data.width/2 + canvas.data.scoreBox /2
    #get bounds for the AI toggle button
    aiLeft = 5 * canvas.data.width/6
    aiRight = canvas.data.width
    #if restart area is pressed, reinitialize the board
    if (event.num == 1 and event.x >= smileyLeft and event.x <= smileyRight
        and event.y <= canvas.data.scoreBox and event.y >= 0):
        init(canvas)
    #if the click is on the grid complete the appropriate move
    elif (event.num == 1 and event.y >= canvas.data.scoreBox
          and canvas.data.gameOver == False):
        completeMove(canvas,row,col)
    #only redraw the board when the game has not been lost or won
    if canvas.data.gameOver == False:
        redrawAll(canvas)

#takes in a row and col and completes the appropriate move
def completeMove(canvas,row,col):
    #if there are no mines around the square, recursively reveal
    #tiles until a mine is reached
    if(canvas.data.bottomLayer[row][col] == 0):
            recursive(canvas,row,col)
            canvas.data.count += 1
    elif(canvas.data.bottomLayer[row][col] != 0):
        #if the click reveals a mine, end the game
        if(canvas.data.bottomLayer[row][col]==-1):
            canvas.data.topLayer[row][col] = -1
            print 'Game Over'
            displayMines(canvas)
            canvas.data.win = 2
            redrawAll(canvas)
            gameOver(canvas)
        #if the click simply reveals a number, display the number
        else:
            canvas.data.topLayer[row][col] = canvas.data.bottomLayer[row][col]
            canvas.data.count += 1

#right-click
def mousePressed2(event,canvas):
    if(event.y >= 0 and event.y <= canvas.data.scoreBox):
        pass
    #grid does not include scoreBox at the top
    row = (event.y - canvas.data.scoreBox)/canvas.data.cellSize
    col = (event.x)/canvas.data.cellSize
    if (event.num == 2 and event.y >= canvas.data.scoreBox
        and canvas.data.gameOver == False):
        #if the clicked space was empty, place a flag
        if canvas.data.topLayer[row][col] == 0:
            canvas.data.topLayer[row][col] = 15
            canvas.data.mines -= 1
            redrawAll(canvas)
        #if the clicked space is a flag, place a question mark
        elif canvas.data.topLayer[row][col] == 15:
            canvas.data.topLayer[row][col] = 12
            canvas.data.mines += 1
        #if the clicked space is a question mark, return back to empty
        elif canvas.data.topLayer[row][col] == 12:
            canvas.data.topLayer[row][col] = 0
    redrawAll(canvas)

#handles key events
def keyPressed(event,canvas):
    #restart game
    if event.char == 'r':
        init(canvas)

#used in testing phases. Prints the bottom layer
def printGrid(canvas):
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            print '%3d'% canvas.data.bottomLayer[row][col],
        print

#recursively reveals as many empty cells as it can
def recursive(canvas,row,col):
    c = canvas
    c.data.topLayer[row][col] = 11
    c.data.bottomLayer[row][col] = 11
    for a in xrange(-1,2):
        for b in xrange(-1,2):
            if((row + a >= 0) and (row + a < c.data.rows) and
               (col + b >= 0) and (col + b < c.data.cols)):
                if(a != 0 or b != 0):
                    #if the cell is empty, keep revealing
                    if(c.data.bottomLayer[row + a][col + b] == 0):
                        recursive(c,row + a, col + b)
                    #otherwise display its number
                    elif(c.data.bottomLayer[row + a][col + b] > 0 and
                         c.data.bottomLayer[row + a][col + b] < 9):
                        c.data.topLayer[row+a][col+b]=c.data.bottomLayer[row+a][col + b]

#display all mines when a mine is clicked
def displayMines(canvas):
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if canvas.data.bottomLayer[row][col] == -1:
                canvas.data.topLayer[row][col] = -1
#called when a game is lost
def gameOver(canvas):
    #reset the click/move count
    canvas.data.count = 0
    canvas.data.gameOver = True
    redrawAll(canvas)

#choose either a smiley, dead, or cool face for the restart button
def pickFace(canvas):
    if canvas.data.win == 0:
        #if game is playing
        return canvas.data.smiley
    elif canvas.data.win == 1:
        #if game is won
        return canvas.data.cool
    else:
        #if game is lost
        return canvas.data.dead

#draw menu on top of the board
def drawMenu(canvas):
    w = canvas.data.width
    s = canvas.data.scoreBox
    face = pickFace(canvas)
    canvas.create_rectangle(0,0,w,s,fill='gray', outline = 'gray')
    canvas.create_rectangle(0,0,w/6,s,fill = 'light slate gray')
    canvas.create_rectangle(5 * w/6,0,w,s,fill = 'light slate gray')
    canvas.create_image(w/2,s/2,image = face)
    #create scoreboard and timer display
    canvas.create_rectangle(w/6, 0, 2 * w/6,s,fill = 'black', outline='white')
    canvas.create_rectangle(4 * w/6, 0, 5 * w/6,s,fill = 'black',
                            outline = 'white')
    canvas.create_text(3 * w/12,s/2,text = str(canvas.data.mines), fill='Red')
    canvas.create_text(9 * w/12,s/2,text = str(canvas.data.time),fill = 'Red')

#redrawAll calls this to draw the board based on each cells' contents
def drawMineBoard(canvas):
    drawMenu(canvas)
    #uses the bottom layer to draw the the top layer
    for row in xrange(len(canvas.data.bottomLayer)):
        for col in xrange(len(canvas.data.bottomLayer[0])):
            if canvas.data.topLayer[row][col] == 0:
                drawMineCell(canvas,row,col)
            elif canvas.data.topLayer[row][col] == 15:
                drawFlag(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 12):
                 drawQuestionMark(canvas,row,col)
            elif canvas.data.topLayer[row][col] == 1:
                drawOne(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 2):
                 drawTwo(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 3):
                drawThree(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 11):
                 drawEmpty(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == -1):
                drawMine(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 4):
                drawFour(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 5):
                drawFive(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 6):
                drawSix(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 7):
                drawSeven(canvas,row,col)
            elif(canvas.data.topLayer[row][col] == 8):
                drawEight(canvas,row,col)

def drawMineCell(canvas, row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.blank, anchor = NW)

def drawMine(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.mine, anchor = NW)

def drawFlag(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.flag, anchor = NW)

def drawQuestionMark(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.qmark, anchor = NW)

def drawOne(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.one, anchor = NW)

def drawTwo(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.two, anchor = NW)

def drawThree(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.three, anchor = NW)

def drawFour(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.four, anchor = NW)

def drawEmpty(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_rectangle(left,top,left + canvas.data.cellSize,
                            top + canvas.data.cellSize, fill = 'gray',
                            outline = 'dim gray')

def drawFive(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.five, anchor = NW)

def drawSix(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.six, anchor = NW)

def drawSeven(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.seven, anchor = NW)

def drawEight(canvas,row,col):
    left = col * canvas.data.cellSize
    top = row * canvas.data.cellSize + canvas.data.scoreBox
    canvas.create_image(left, top, image = canvas.data.eight, anchor = NW)

#checks for a win every time scoreTime is fired
def checkMines(canvas):
    flagCount = 0
    mineCount = 0
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if canvas.data.topLayer[row][col] != 0:
                if ((canvas.data.topLayer[row][col] == 15 or
                     canvas.data.topLayer[row][col] == 0)
                    and canvas.data.bottomLayer[row][col] == -1):
                    mineCount += 1
    #only way to win is when all the mines are flagged
    if mineCount == countMines(canvas) and mineCount != 0:
        print 'YOU WIN'
        canvas.data.win = 1
        #reveal all the mines
        finishBoard(canvas)
        redrawAll(canvas)
        canvas.data.gameOver = True
        #display a win message
        winScreen(canvas)

#count the total number of mines in the board
def countMines(canvas):
    count = 0
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if canvas.data.bottomLayer[row][col] == -1:
                count += 1
    return count
    
def redrawAll(canvas):
    canvas.delete(ALL)
    drawMineBoard(canvas)

#calculates the total percentage of tiles that have been revealed
def percentRevealed(canvas):
    count = 0
    for r in xrange(canvas.data.rows):
        for c in xrange(canvas.data.cols):
            if (canvas.data.topLayer[r][c] < 12
                and canvas.data.topLayer[r][c] != 0):
                count += 1
    return count * 1.0 /(canvas.data.rows**2)

#counts the number of blank unrevealed cells in the board
def countBlank(canvas):
    count = 0
    for r in xrange(canvas.data.rows):
        for c in xrange(canvas.data.cols):
            if canvas.data.topLayer[r][c] == 0:
                count += 1
    return count

#loops through board and revels all the mines and other values
def finishBoard(canvas):
    c = canvas
    print 'finishing..'
    for row in xrange(c.data.rows):
        for col in xrange(c.data.cols):
            if(c.data.bottomLayer[row][col] == 0):
                recursive(c,row,col)
            elif(c.data.bottomLayer[row][col] != 0
                 and c.data.bottomLayer[row][col] != -1):
                c.data.topLayer[row][col]=c.data.bottomLayer[row][col]

#displayed when the game is won
def winScreen(canvas):
    canvas.data.delay = 1000
    canvas.data.count = 0

#calculates number of flags placed by the AI
def flagPercentage(canvas):
    count = 0
    for row in xrange(canvas.data.rows):
        for col in xrange(canvas.data.cols):
            if canvas.data.topLayer[row][col] == 15:
                count += 1
    return 1.0 * count / canvas.data.totalMines * 100

#uses PIL to load the faces for the restart button
def loadFaces(canvas):
    im = Image.open('tao-smile.gif')
    im = im.resize((canvas.data.scoreBox,canvas.data.scoreBox),Image.ANTIALIAS)
    smiley = ImageTk.PhotoImage(im)
    canvas.data.smiley = smiley
    im = Image.open('tao-dead.gif')
    im = im.resize((canvas.data.scoreBox,canvas.data.scoreBox),Image.ANTIALIAS)
    dead = ImageTk.PhotoImage(im)
    canvas.data.dead = dead
    im = Image.open('tao-cool.gif')
    im = im.resize((canvas.data.scoreBox,canvas.data.scoreBox),Image.ANTIALIAS)
    cool = ImageTk.PhotoImage(im)
    canvas.data.cool = cool

#uses PIL to load flags, mines, question marks, and blank squares
def loadNonNumbers(canvas):
    im = Image.open('Qmark.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    Qmark = ImageTk.PhotoImage(im)
    canvas.data.qmark = Qmark
    im = Image.open('flag.gif')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    flag = ImageTk.PhotoImage(im)
    canvas.data.flag = flag
    im = Image.open('Blank.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    blank = ImageTk.PhotoImage(im)
    canvas.data.blank = blank
    im = Image.open('mine.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    mine = ImageTk.PhotoImage(im)
    canvas.data.mine = mine

#uses PIL to load all numbers
def loadNumbers(canvas):
    im = Image.open('one.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.one = one = ImageTk.PhotoImage(im)
    im = Image.open('two.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.two = two =  ImageTk.PhotoImage(im)
    im = Image.open('three.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.three = three = ImageTk.PhotoImage(im)
    im = Image.open('four.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.four = four = ImageTk.PhotoImage(im)
    im = Image.open('five.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.five = five = ImageTk.PhotoImage(im)
    im = Image.open('six.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.six = six = ImageTk.PhotoImage(im)
    im = Image.open('seven.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.seven = seven = ImageTk.PhotoImage(im)
    im = Image.open('eight.jpg')
    im = im.resize((canvas.data.cellSize,canvas.data.cellSize),Image.ANTIALIAS)
    canvas.data.eight = eight = ImageTk.PhotoImage(im)

#loads all the variables needed. also used when restarting game
def init(canvas):
    loadFaces(canvas)
    loadNonNumbers(canvas)
    loadNumbers(canvas)
    canvas.data.count,canvas.data.autoCount = 0,0
    canvas.data.mines = canvas.data.totalMines
    canvas.data.win,canvas.data.time,canvas.data.score = 0,0,0
    canvas.data.aiLevel = ''
    canvas.data.originalAuto = False
    canvas.data.gameOver = False
    canvas.data.delay = 1000
    canvas.data.isAuto = False
    canvas.data.stopGame = False
    canvas.data.autoDelay = canvas.data.delay
    canvas.data.bottomLayer = [[0 for col in xrange(canvas.data.cols)]
                               for row in xrange(canvas.data.rows)]
    canvas.data.topLayer = [[0 for col in xrange(canvas.data.cols)]
                               for row in xrange(canvas.data.rows)]
    bomb_matrix = create_matrix(canvas, rows, cols, mines)
    if debug:
        print bomb_matrix
        print "number of rows = %i" % len(bomb_matrix)
        print "number of columns = %i" % len(bomb_matrix[0])
    replace_bomb_count(canvas, bomb_matrix)

    redrawAll(canvas)
    drawMineBoard(canvas)

# set default size
cols = 30
rows = 16
name = "Pat"
mines = 30

root = Tk()
#create canvas
scoreBox,cellSize = 40,30
canvasWidth = cols*cellSize
canvasHeight = rows*cellSize + scoreBox

canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
canvas.pack()
root.canvas = canvas.canvas = canvas
class Struct: pass
canvas.data = Struct()

#initialize variables
canvas.data.rows,canvas.data.cols,canvas.data.name = rows,cols,name
canvas.data.width,canvas.data.height = canvasWidth,canvasHeight
canvas.data.mines,canvas.data.totalMines = mines,mines
canvas.data.scoreBox,canvas.data.cellSize = scoreBox,cellSize
init(canvas)

redrawAll(canvas)

#create wrapper functions for events
def mousePressedFn1(event): mousePressed1(event,canvas)
def mousePressedFn2(event): mousePressed2(event,canvas)
root.bind("<Button-2>", mousePressedFn2)
root.bind("<Button-1>", mousePressedFn1)
def keyPressedFn(event): keyPressed(event,canvas)
root.bind("<Key>", keyPressedFn) 
#start timer display's timer fired
scoreTime(canvas)#initialize AI's timer
#timerFired(canvas)
root.mainloop()  # This call BLOCKS 


