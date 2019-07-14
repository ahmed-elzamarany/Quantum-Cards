
import random, pygame, sys
from pygame.locals import *
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, execute, Aer
from qiskit.tools.visualization import circuit_drawer
from qiskit.quantum_info import state_fidelity
from qiskit import BasicAer

simulator = Aer.get_backend('qasm_simulator')
FPS = 30 # frames per second, the general speed of the program
WINDOWWIDTH = 960 # size of window's width in pixels
WINDOWHEIGHT = 720 # size of windows' height in pixels
REVEALSPEED = 8 # speed boxes' sliding reveals and covers
BOXSIZE = 40 # size of box height & width in pixels
GAPSIZE = 10 # size of gap between boxes in pixels
buttonNextWidth=12*WINDOWWIDTH // 16
buttonNextHeight=15*WINDOWHEIGHT//16
buttonBackWidth=1*WINDOWWIDTH // 16
buttonBackHeight=15*WINDOWHEIGHT//16
buttonMeasureHeight=2*WINDOWHEIGHT//16
buttonEtalHeight=2*WINDOWHEIGHT//16
buttonEtalWidth=buttonBackWidth
buttonModeWidth=(WINDOWWIDTH - 160) // 2
buttonModeHeight= (WINDOWHEIGHT-40)
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK     = (0, 0, 0)

BGCOLOR = WHITE
LIGHTBGCOLOR = GRAY
HIGHLIGHTCOLOR = BLUE
Arrow = 'arrow.jpg'
DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

qubits=["000","001","010","011","100","101","110","111"]
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
def main():
    global FPSCLOCK, DISPLAYSURF ,BOARDWIDTH ,BOARDHEIGHT ,level,Shapes, revealedBoxes ,BOXCOLOR,score
    BOARDWIDTH = 2 # number of columns of icons
    BOARDHEIGHT = 2 # number of rows of icons
    gameInt(BOARDWIDTH,BOARDHEIGHT)
    pygame.init()
    pygame.font.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    Ental=False
         
    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Quantum-Cards')
    level =1
    Shapes = generateShapes()
    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)
    score=0
    firstSelection = None # stores the (x, y) of the first box clicked.
    secondSelection = None
    NextISClicked=False
    Mode = False

    while True: # main game loop
        mouseClicked = False
        color1= None
        color2= None
        arrow= None
        if NextISClicked :
            BOARDWIDTH =2**level # number of columns of icons
            BOARDHEIGHT = 2**level
            gameInt(BOARDWIDTH,BOARDHEIGHT)
            mainBoard = getRandomizedBoard()
            Shapes = generateShapes()
            revealedBoxes = generateRevealedBoxesData(False)
            NextISClicked=False
        if Mode ==True :
            color1=WHITE
            color2=BLACK
            arrow= pygame.image.load('./arrow_inverted.png').convert_alpha()
        else:
            color1=BLACK
            color2=WHITE
            arrow= pygame.image.load('./arrow.png').convert_alpha()

        GUI(color1,color2,arrow)
        BOXCOLOR = color1
        drawBoard(mainBoard, revealedBoxes)
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
     
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        if boxx== "Back" and boxy== None and mouseClicked:
            if level > 1:
                level=level-1
                NextISClicked=True
        elif boxx== "Mode" and boxy== None and mouseClicked:
            Mode=not Mode
        elif boxx== "Ental" and boxy== None and mouseClicked:
            if score>0 :
                Ental=True
                score=score-1
        elif boxx=="Next" and boxy== None and mouseClicked:
            if level<3:
                level=level+1
                NextISClicked=True
        elif  boxx=="Measure" and boxy== None and mouseClicked and secondSelection :

            if Ental:
                qc1=QuantumEntangelte(level)
                qc2=QuantumEntangelte(level)
                Ental=False
            else:
                qc1=QuantumCirct(level)
                qc2=QuantumCirct(level)
            icon1shape, icon1color = getShape(Measure(qc1),Shapes)
            icon2shape, icon2color = getShape(Measure(qc2),Shapes)
            mainBoard[firstSelection[0]][firstSelection[1]]=(icon1shape, icon1color)
            mainBoard[secondSelection[0]][secondSelection[1]]=(icon2shape, icon2color)
            revealBoxesAnimation(mainBoard, [firstSelection])
            revealBoxesAnimation(mainBoard, [secondSelection])
            revealedBoxes[firstSelection[0]][firstSelection[1]] = True
            revealedBoxes[secondSelection[0]][secondSelection[1]] = True

            if icon1shape != icon2shape or icon1color != icon2color:
                # Icons don't match. Re-cover up both selections.
                pygame.time.wait(1000) # 1000 milliseconds = 1 sec
                coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (secondSelection[0], secondSelection[1])])
                revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                revealedBoxes[secondSelection[0]][secondSelection[1]] = False
            elif hasWon(revealedBoxes): # check if all pairs found
                gameWonAnimation(mainBoard)
                pygame.time.wait(2000)

                        # Reset the board
                mainBoard = getRandomizedBoard()
                Shapes = generateShapes()
                revealedBoxes = generateRevealedBoxesData(False)

                        # Show the fully unrevealed board for a second.
                drawBoard(mainBoard, revealedBoxes)
                pygame.display.update()
                pygame.time.wait(1000)
                score=score+10
                        # Replay the start game animation.
            firstSelection = None # reset firstSelection variable
            secondSelection= None
        elif boxx != None and boxy != None:
            # The mouse is currently over a box.
            if not revealedBoxes[boxx][boxy]:
                drawHighlightBox(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else: # the current box was the second box clicked
                    # Check if there is a match between the two icons.
                    secondSelection = (boxx, boxy)
                            # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def gameInt(BOARDWIDTH,BOARDHEIGHT):
    assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'
    global XMARGIN,YMARGIN
    XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
    YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

def GUI(color1,color2,arrow):
        DISPLAYSURF.fill(color2) # drawing the window
        DISPLAYSURF.blit(button("",buttonNextWidth,buttonNextHeight,160,40,color2,ORANGE,color2),(buttonNextWidth+16, buttonNextHeight+8))
        DISPLAYSURF.blit(button("",buttonBackWidth,buttonBackHeight,160,40,color2,ORANGE,color2),(buttonBackWidth+16, buttonBackWidth+8))
        myfont = pygame.font.SysFont('Comic Sans MS', 30)

        text = myfont.render('CAN YOU WIN ??', False,color1) 
        rightArrow = arrow
        rightArrow = pygame.transform.scale(rightArrow, (160, 40))
        DISPLAYSURF.blit(rightArrow,(buttonNextWidth, buttonNextHeight))
        leftArrow = pygame.transform.rotate(rightArrow, 180)
        DISPLAYSURF.blit(leftArrow,(buttonBackWidth, buttonBackHeight))
        DISPLAYSURF.blit(text,((WINDOWWIDTH - text.get_width()) // 2, 0))
        DISPLAYSURF.blit(button("Mode",buttonModeWidth, buttonModeHeight,160,40,color1,ORANGE,color2),(buttonModeWidth+55, (buttonModeHeight)+15))
        DISPLAYSURF.blit(button("Measure",buttonNextWidth,buttonMeasureHeight,160,40,color1,ORANGE,color2),(buttonNextWidth+(( 160) // 4), buttonMeasureHeight+(( 40) // 4)))
        DISPLAYSURF.blit(button("entanglement",buttonEtalWidth,buttonEtalHeight,160,40,color1,ORANGE,color2),(buttonEtalWidth+(( 160) // 16), buttonMeasureHeight+(( 40) // 5)))
        TextLevel=myfont.render("Level:"+str(level), False,color1)   
        scoreText = myfont.render("Score:"+str(score), False,color1) 
        counter=0
        loop =2**level
        for x in range(loop): #Showing the meaning of the shapes
            i = qubits[x]
            qubit1Text = myfont.render(i+":", False,color1) 
            DISPLAYSURF.blit(qubit1Text,(0, 200+qubit1Text.get_height()*counter))
            shape, color = getShape(i,Shapes)
            draw(shape, color, 20+qubit1Text.get_width(), 200+qubit1Text.get_height()*counter)
            counter=counter+1
        DISPLAYSURF.blit(scoreText,(WINDOWWIDTH-120, 0))
        DISPLAYSURF.blit(TextLevel,(0, 0))
        

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes

def QuantumEntangelte(val):
    q0 = QuantumRegister(1)
    c0 = ClassicalRegister(1)
    q1 = QuantumRegister(1)
    c1 = ClassicalRegister(1)
    q2 = QuantumRegister(1)
    c2 = ClassicalRegister(1)
    if val==2:
        t = QuantumCircuit(q0, q1, c0, c1)
        t.h(q0)
        t.cx(q0,q1)
        t.measure(q0, c0)
        t.measure(q1, c1)
        return t
    elif val==3:
        t = QuantumCircuit(q0, q1,q2, c0, c1,c2)
        t.h(q0)
        t.cx(q0,q1)
        t.cx(q0,q2)
        t.measure(q0, c0)
        t.measure(q1, c1)
        t.measure(q2, c2)
        return t
    return QuantumCirct(val)


def QuantumCirct (val):
    circ = QuantumCircuit()
    for i in range(val):
        t = QuantumCircuit()
        q0 = QuantumRegister(1)
        c0 = ClassicalRegister(1)
        t.add_register(q0)
        t.add_register(c0)
        t.h(q0)
        t.measure(q0, c0)
        circ = circ + t
    # circ.draw(filename=r'C:\Users\ahmed\Documents\projects\quantum_relm\Bohr\try.jpg',output='mpl')
    return circ


def Measure (circ):
    job2 = execute(circ, simulator, shots=1, memory=True)
    counts = job2.result().get_memory(circ)
    
    return counts[0].replace(" ", "")

def generateShapes():
    # Get a list of every possible shape in every possible color.
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = 2**level
    icons = icons[:numIconsUsed] 
    random.shuffle(icons)
    return icons
    
def getShape(val,shapes):
    return shapes[int(val,2)]

def getRandomizedBoard():
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(Shapes[0])
        board.append(column)
    
    return board


def splitIntoGroupsOf(groupSize, theList):
    # splits a list into a list of lists, where the inner lists have at
    # most groupSize number of items.
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)
    

def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)

    boxRect = pygame.Rect(buttonNextWidth, buttonNextHeight, 160, 40)
    if boxRect.collidepoint(x, y):
        return ("Next",None)
    boxRect = pygame.Rect(buttonNextWidth, buttonMeasureHeight, 160, 40)
    if boxRect.collidepoint(x, y):
        return ("Measure",None)
    boxRect = pygame.Rect(buttonEtalWidth, buttonEtalHeight, 160, 40)
    if boxRect.collidepoint(x, y):
        return ("Ental",None)
    boxRect = pygame.Rect(buttonModeWidth, buttonModeHeight, 160, 40)
    if boxRect.collidepoint(x, y):
        return ("Mode",None)
    boxRect = pygame.Rect(buttonBackWidth, buttonBackHeight, 160, 40)
    if boxRect.collidepoint(x, y):
        return ("Back",None)
    return (None, None)

def draw(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = (boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))
    


def getShapeAndColor(board, boxx, boxy):
    # shape value for x, y spot is stored in board[x][y][0]
    # color value for x, y spot is stored in board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    # Draws boxes being covered/revealed. "boxes" is a list
    # of two-item lists, which have the x & y spot of the box.
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: # only draw the cover if there is an coverage
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    # Do the "box reveal" animation.
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    # Do the "box cover" animation.
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    # Draws all of the boxes in their covered or revealed state.
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box.
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon.
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    # Randomly reveal the boxes 8 at a time.
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(8, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        revealBoxesAnimation(board, boxGroup)
        coverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    # flash the background color when the player has won
    coveredBoxes = generateRevealedBoxesData(True)
    color1 = LIGHTBGCOLOR
    color2 = BGCOLOR

    for i in range(13):
        color1, color2 = color2, color1 # swap colors
        DISPLAYSURF.fill(color1)
        drawBoard(board, coveredBoxes)
        pygame.display.update()
        pygame.time.wait(300)


def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        if False in i:
            return False # return False if any boxes are covered.
    return True

def button(msg,x,y,w,h,ic,ac,color2):
    mouse = pygame.mouse.get_pos()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(DISPLAYSURF, ac,(x,y,w,h))
    else:
        pygame.draw.rect(DISPLAYSURF, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf =smallText.render(msg, True,color2 ) 
    textRect = textSurf.get_rect() 
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    return textSurf

if __name__ == '__main__':
    main()