import random
class GameState():
    def __init__(self):
        
        
        self.board = [
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","bp","--","--","--","--"],
            ["bp","--","--","--","--","--","--","--"],
            ["--","--","--","wp","--","--","--","--"],
            ["--","--","--","wp","--","--","--","--"],
            ["wp","--","--","--","wp","--","wp","wp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"]]
        self.board = [
            ["--","bp","--","bp","--","bp","--","bp"],
            ["bp","--","bp","--","bp","--","bp","--"],
            ["--","bp","--","bp","--","bp","--","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","--","wp","--","wp","--","wp","--"],
            ["--","wp","--","wp","--","wp","--","wp"],
            ["wp","--","wp","--","wp","--","wp","--"]]
        
        self.whiteToMove = True
        self.moveLog = []
        self.turnLog = []
    def makeJumpMove(self,move):
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        #disappear jumpedpiece
        if (move.startRow - move.endRow == 2) and (move.startCol - move.endCol == 2):
            self.board[move.startRow-1][move.startCol-1] = "--"
        elif (move.startRow - move.endRow == 2) and (move.startCol - move.endCol == -2):
            self.board[move.startRow-1][move.startCol+1] = "--"

        elif (move.startRow - move.endRow == -2) and (move.startCol - move.endCol == 2):
            self.board[move.startRow+1][move.startCol-1] = "--"
        elif (move.startRow - move.endRow == -2) and (move.startCol - move.endCol == -2):
            self.board[move.startRow+1][move.startCol+1] = "--"  
        self.whiteToMove = not self.whiteToMove
    
    def makeMove(self,move):
        self.turnLog.append(self.whiteToMove)
        if not move.jump:
            self.board[move.startRow][move.startCol] = '--'
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            #promotion
            if move.pieceMoved == "wp":
                if move.endRow == 0:
                    self.board[move.endRow][move.endCol] = "wQ"
                
            elif move.pieceMoved == "bp":
                if move.endRow == 7:
                    self.board[move.endRow][move.endCol] = "bQ"
                
            self.whiteToMove = not self.whiteToMove
        else:
            self.board[move.startRow][move.startCol] = '--'
            self.board[move.endRow][move.endCol] = move.pieceMoved
            self.moveLog.append(move)
            #emptying jumped square
            if (move.startRow - move.endRow == 2) and (move.startCol - move.endCol == 2):
                self.board[move.startRow-1][move.startCol-1] = "--"
            elif (move.startRow - move.endRow == 2) and (move.startCol - move.endCol == -2):
                self.board[move.startRow-1][move.startCol+1] = "--"

            elif (move.startRow - move.endRow == -2) and (move.startCol - move.endCol == 2):
                self.board[move.startRow+1][move.startCol-1] = "--"
            elif (move.startRow - move.endRow == -2) and (move.startCol - move.endCol == -2):
                self.board[move.startRow+1][move.startCol+1] = "--"
            #promotion
            if move.pieceMoved == "wp":
                if move.endRow == 0:
                    self.board[move.endRow][move.endCol] = "wQ"
                
            elif move.pieceMoved == "bp":
                if move.endRow == 7:
                    self.board[move.endRow][move.endCol] = "bQ"
            
            if not self.isJumpPossible(self.board):
                self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.whiteToMove=self.turnLog.pop()
            if not move.jump:
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = "--"

            else:
                self.board[move.startRow][move.startCol] = move.pieceMoved
                self.board[move.endRow][move.endCol] = "--"
                #jumped piece
                if (move.startRow - move.endRow == 2) and (move.startCol - move.endCol == 2):
                    self.board[move.startRow-1][move.startCol-1] = move.pieceJumped
                elif (move.startRow - move.endRow == 2) and (move.startCol - move.endCol == -2):
                    self.board[move.startRow-1][move.startCol+1] = move.pieceJumped

                elif (move.startRow - move.endRow == -2) and (move.startCol - move.endCol == 2):
                    self.board[move.startRow+1][move.startCol-1] = move.pieceJumped
                elif (move.startRow - move.endRow == -2) and (move.startCol - move.endCol == -2):
                    self.board[move.startRow+1][move.startCol+1] = move.pieceJumped
             
    def getAllPossibleMoves(self):
        moves = []
        if self.isJumpPossible(self.board):
            for r in range(len(self.board)):
                for c in range(len(self.board[r])):
                    if (self.board[r][c][0] == 'w' and self.whiteToMove) or (self.board[r][c][0] == 'b' and not self.whiteToMove):
                        if self.board[r][c][1] == "p":
                            self.getPawnJumpMoves(r,c,moves)
                        else:
                            self.getQueenJumpMoves(r,c,moves)
            return moves   
        else:
            for r in range(len(self.board)):
                for c in range(len(self.board[r])):
                    if (self.board[r][c][0] == 'w' and self.whiteToMove) or (self.board[r][c][0] == 'b' and not self.whiteToMove):
                        if self.board[r][c][1] == "p":
                            self.getPawnMoves(r,c,moves)
                        else:
                            self.getQueenMoves(r,c,moves)
            return moves

    def getPawnMoves(self,r,c,moves):
        if self.whiteToMove:
            if r-1 >= 0 and c-1 >= 0:    
                if self.board[r-1][c-1] == '--':
                    moves.append(Move((r,c), (r-1,c-1), self.board))        
            if r-1 >= 0 and c+1 <= 7:
                if self.board[r-1][c+1] == '--':
                    moves.append(Move((r,c), (r-1,c+1), self.board)) 
        else:
            if r+1 <= 7 and c-1 >= 0:    
                if self.board[r+1][c-1] == '--':
                    moves.append(Move((r,c), (r+1,c-1), self.board))        
            if r+1 <= 7 and c+1 <= 7:
                if self.board[r+1][c+1] == '--':
                    moves.append(Move((r,c), (r+1,c+1), self.board))
                
    def getPawnJumpMoves(self,r,c,moves):
        if self.whiteToMove:
            if (r-2 >= 0) and (c-2 >= 0):
                if self.board[r-1][c-1][0] == 'b' and self.board[r-2][c-2] == "--":
                    moves.append(Move((r,c), (r-2,c-2), self.board))   
            if (r-2 >= 0) and (c+2 <= 7): 
                if self.board[r-1][c+1][0] == 'b' and self.board[r-2][c+2] == "--":
                    moves.append(Move((r,c), (r-2,c+2), self.board))
        else:
            if (r+2 <= 7) and (c-2 >= 0):
                if self.board[r+1][c-1][0] == 'w' and self.board[r+2][c-2] == "--":
                    moves.append(Move((r,c), (r+2,c-2), self.board))   
            if (r+2 <= 7) and (c+2 <= 7): 
                if self.board[r+1][c+1][0] == 'w' and self.board[r+2][c+2] == "--":
                    moves.append(Move((r,c), (r+2,c+2), self.board))
                         
    def getQueenMoves(self,r,c,moves):
        if r-1 >= 0 and c-1 >= 0:    
            if self.board[r-1][c-1] == '--':
                moves.append(Move((r,c), (r-1,c-1), self.board))        
        if r-1 >= 0 and c+1 <= 7:
            if self.board[r-1][c+1] == '--':
                moves.append(Move((r,c), (r-1,c+1), self.board)) 
        if r+1 <= 7 and c-1 >= 0:    
            if self.board[r+1][c-1] == '--':
                moves.append(Move((r,c), (r+1,c-1), self.board))        
        if r+1 <= 7 and c+1 <= 7:
            if self.board[r+1][c+1] == '--':
                moves.append(Move((r,c), (r+1,c+1), self.board)) 
        
    def getQueenJumpMoves(self,r,c,moves):
        if self.whiteToMove:
            if (r-2 >= 0) and (c-2 >= 0):#forward
                if self.board[r-1][c-1][0] == 'b' and self.board[r-2][c-2] == "--":
                    moves.append(Move((r,c), (r-2,c-2), self.board))   
            if (r-2 >= 0) and (c+2 <= 7): 
                if self.board[r-1][c+1][0] == 'b' and self.board[r-2][c+2] == "--":
                    moves.append(Move((r,c), (r-2,c+2), self.board))
            
            if (r+2 <= 7) and (c-2 >= 0):#backward
                if self.board[r+1][c-1][0] == 'b' and self.board[r+2][c-2] == "--":
                    moves.append(Move((r,c), (r+2,c-2), self.board))   
            if (r+2 <= 7) and (c+2 <= 7): 
                if self.board[r+1][c+1][0] == 'b' and self.board[r+2][c+2] == "--":
                    moves.append(Move((r,c), (r+2,c+2), self.board))
        else:
            if (r-2 >= 0) and (c-2 >= 0):#forward
                if self.board[r-1][c-1][0] == 'w' and self.board[r-2][c-2] == "--":
                    moves.append(Move((r,c), (r-2,c-2), self.board))   
            if (r-2 >= 0) and (c+2 <= 7): 
                if self.board[r-1][c+1][0] == 'w' and self.board[r-2][c+2] == "--":
                    moves.append(Move((r,c), (r-2,c+2), self.board))

            if (r+2 <= 7) and (c-2 >= 0):#backward
                if self.board[r+1][c-1][0] == 'w' and self.board[r+2][c-2] == "--":
                    moves.append(Move((r,c), (r+2,c-2), self.board))   
            if (r+2 <= 7) and (c+2 <= 7): 
                if self.board[r+1][c+1][0] == 'w' and self.board[r+2][c+2] == "--":
                    moves.append(Move((r,c), (r+2,c+2), self.board))
    
    def isJumpPossible(self,board):
        if self.whiteToMove:
            for r in range(len(board)):
                for c in range(len(board[r])):
                    #pawn için
                    if board[r][c]=="wp":
                        if (r-2 >= 0) and (c-2 >= 0):
                            if self.board[r-1][c-1][0] == 'b' and self.board[r-2][c-2] == "--":
                                return True  
                        if (r-2 >= 0) and (c+2 <= 7): 
                            if self.board[r-1][c+1][0] == 'b' and self.board[r-2][c+2] == "--":
                                return True
                    #queen için
                    if board[r][c]=="wQ":
                        if (r-2 >= 0) and (c-2 >= 0):#forward
                            if self.board[r-1][c-1][0] == 'b' and self.board[r-2][c-2] == "--":
                                return True     
                        if (r-2 >= 0) and (c+2 <= 7): 
                            if self.board[r-1][c+1][0] == 'b' and self.board[r-2][c+2] == "--":
                                return True  
                
                        if (r+2 <= 7) and (c-2 >= 0):#backward
                            if self.board[r+1][c-1][0] == 'b' and self.board[r+2][c-2] == "--":
                                return True     
                        if (r+2 <= 7) and (c+2 <= 7): 
                            if self.board[r+1][c+1][0] == 'b' and self.board[r+2][c+2] == "--":
                                return True  
        else:
            for r in range(len(board)):
                for c in range(len(board[r])):
                    #pawn için
                    if board[r][c]=="bp":
                        if (r+2 <= 7) and (c-2 >= 0):
                            if self.board[r+1][c-1][0] == 'w' and self.board[r+2][c-2] == "--":
                                return True
                        if (r+2 <= 7) and (c+2 <= 7): 
                            if self.board[r+1][c+1][0] == 'w' and self.board[r+2][c+2] == "--":
                                return True
                    #queen için
                    if board[r][c]=="bQ":
                        if (r-2 >= 0) and (c-2 >= 0):#forward
                            if self.board[r-1][c-1][0] == 'w' and self.board[r-2][c-2] == "--":
                                return True   
                        if (r-2 >= 0) and (c+2 <= 7): 
                            if self.board[r-1][c+1][0] == 'w' and self.board[r-2][c+2] == "--":
                                return True

                        if (r+2 <= 7) and (c-2 >= 0):#backward
                            if self.board[r+1][c-1][0] == 'w' and self.board[r+2][c-2] == "--":
                                return True   
                        if (r+2 <= 7) and (c+2 <= 7): 
                            if self.board[r+1][c+1][0] == 'w' and self.board[r+2][c+2] == "--":
                                return True
        return False

class Move():
    
    def __init__(self, startSq, endSq, board, jump=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]        
        self.endRow = endSq[0]    
        self.endCol = endSq[1]  
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol] 
        
        self.pieceJumped = board[0][0]#####
        self.jump=jump
        
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
    
        if abs(self.endCol - self.startCol) == 2:#jump control and piece jumped
            self.jump = True
            if (self.startRow - self.endRow == 2) and (self.startCol - self.endCol == 2):
                self.pieceJumped = board[self.startRow-1][self.startCol-1]
            elif (self.startRow - self.endRow == 2) and (self.startCol - self.endCol == -2):
                self.pieceJumped = board[self.startRow-1][self.startCol+1]

            elif (self.startRow - self.endRow == -2) and (self.startCol - self.endCol == 2):
                self.pieceJumped = board[self.startRow+1][self.startCol-1]
            elif (self.startRow - self.endRow == -2) and (self.startCol - self.endCol == -2):
                self.pieceJumped = board[self.startRow+1][self.startCol+1]

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID  
        return False  
    