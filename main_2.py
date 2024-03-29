import pygame as p
import engine_2

BOARD_WIDTH = BOARD_HEIGHT = 512
DIMENSION = 8
SQ_SIZE = BOARD_HEIGHT//DIMENSION
MAX_FPS = 15 
IMAGES = {}

def loadImages():
    pieces = ['wp','wQ','bp','bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("C:/Users/Alper/Desktop/dama/images/"+piece+".png"), (SQ_SIZE,SQ_SIZE))

def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH , BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = engine_2.GameState()
    allPossibleMoves = gs.getAllPossibleMoves()
    moveMade=False
    loadImages()
    running = True 
    sqSelected = ()
    playerClicks = []   
    gameOver = False

    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
                
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location = p.mouse.get_pos() ###
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row,col):
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected)
                    if len(playerClicks) == 2:
                        move = engine_2.Move(playerClicks[0], playerClicks[1], gs.board)
                        if move in allPossibleMoves:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = ()
                            playerClicks = []
                        else:
                            playerClicks = [sqSelected]
            
            
            
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    gameOver = False

        if moveMade:
            allPossibleMoves = gs.getAllPossibleMoves()
            moveMade = False
        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color('gray')]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()