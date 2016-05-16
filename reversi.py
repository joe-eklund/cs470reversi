from Tkinter import *
import Tkinter as tk
import tkMessageBox

class Reversi:
    board = []
    pieces = []
    previewPiece = None
    turn = "white"
    validPositions = []

    def __init__(self, master):
        self.debug = True
        if self.debug: print 'Starting up game.'
        # Initialize window
        self.master = master
        master.title("Reversi")

        # New game button
        self.greet_button = Button(master, text="Start New Game", command=self.initializeBoard)
        self.greet_button.pack()

        labelframe = tk.Frame()
        self.whiteScore = tk.Label(labelframe,text="White Score: 2", relief=SUNKEN)
        self.blackScore = tk.Label(labelframe,text=" || Black Score: 2", relief=SUNKEN)
        # Turn Label
        self.turnLabel = tk.Label(labelframe, text="",relief=SUNKEN)

        self.whiteScore.grid(row=0, column=0)
        self.turnLabel.grid(row=0, column=1)
        self.blackScore.grid(row=0, column=2)
        labelframe.pack()

        # Game Board
        self.canvas = Canvas(root, bg="darkgreen", height=640, width=640)
        self.canvas.bind("<Configure>", self.draw)
        self.canvas.bind("<Leave>", self.onLeave)
        self.board = [[None for x in range(8)] for y in range(8)]
        for i in range(8):
            for j in range(8):
                self.board[i][j] = self.canvas.create_rectangle(0, 0, 0, 0, fill="darkgreen", tags="rectangle")
        self.canvas.tag_bind("rectangle", "<Enter>", self.onEnter)
        self.canvas.tag_bind("rectangle", "<Button-1>", self.selectPosition)
        self.canvas.pack(fill=BOTH, expand=YES)

        # Auto start a game
        self.initializeBoard()

    # Bring the board to it's starting state
    def initializeBoard(self):
        if self.debug: print 'Initializing board.'
        self.turn = "white"
        self.canvas.delete("piece") #Added to delete all the pieces when we click new game. 
        self.pieces = [[None for x in range(8)] for y in range(8)]
        self.pieces[3][3] = self.canvas.create_oval(0, 0, 0, 0, fill="white", tags=("piece","white"))
        self.pieces[3][4] = self.canvas.create_oval(0, 0, 0, 0, fill="black", tags=("piece","black"))
        self.pieces[4][3] = self.canvas.create_oval(0, 0, 0, 0, fill="black", tags=("piece","black"))
        self.pieces[4][4] = self.canvas.create_oval(0, 0, 0, 0, fill="white", tags=("piece","white"))
        self.canvas.tag_bind("piece", "<Enter>", self.onEnter)
        self.toggleTurn()
        self.draw(None)

    # Redraw the board
    def draw(self, event):
        if self.debug: print 'Redrawing board.'
        width = self.canvas.winfo_width() - 1
        height = self.canvas.winfo_height() - 1
        for i in range(8):
            for j in range(8):
                self.canvas.coords(self.board[i][j], (width / 8.0) * i, (height / 8.0) * j,
                                   (width / 8.0) * (i + 1), (height / 8.0) * (j + 1))
                if self.pieces[i][j] is not None:
                    self.canvas.coords(self.pieces[i][j], (width / 8.0) * i, (height / 8.0) * j,
                                       (width / 8.0) * (i + 1), (height / 8.0) * (j + 1))

    # fires when a square of the board or the preview piece is clicked
    def selectPosition(self, event):
        x, y = self.getBoardPos(event.x, event.y)
        square = self.board[x][y]
        if self.debug: print 'Position selected: [' + str(x) + ', ' + str(y) + ']'
        piece = self.pieces[x][y]  # Piece may be null(None)
        if self.previewPiece is not None:
            self.canvas.delete(self.previewPiece)
            self.previewPiece = None
            self.placePieceAndReverseColors(x, y)
            self.toggleTurn()

    # fires when the mouse enters a square of the board
    def onEnter(self, event):
        x, y = self.getBoardPos(event.x, event.y)
        #if self.debug: print 'Position hovered: [' + str(x) + ', ' + str(y) + ']'
        square = self.board[x][y]
        piece = self.pieces[x][y]  # Piece may be null(None)
        color = "gray"
        if self.turn == "black":
            color = "gray20"
        self.canvas.delete(self.previewPiece)
        self.previewPiece = None
        if self.validPositions.__contains__([x, y]):
            self.previewPiece = self.canvas.create_oval(self.canvas.coords(square), fill=color)
            self.canvas.tag_bind(self.previewPiece, "<Button-1>", self.selectPosition)

    # fires when the mouse leaves the board
    def onLeave(self, event):
        x, y = self.getBoardPos(event.x, event.y)
        #if self.debug: print 'Position left: [' + str(x) + ', ' + str(y) + ']'
        square = event.widget.find_closest(event.x, event.y)[0]
        self.canvas.delete(self.previewPiece)
        self.previewPiece = None

    # Get the board position that the mouse is in
    def getBoardPos(self, x, y):
        xQuad = (int)(x / (self.canvas.winfo_width() / 8.0))
        yQuad = (int)(y / (self.canvas.winfo_height() / 8.0))
        return xQuad, yQuad

    # Change the turn from white to black or black to white
    def toggleTurn(self):
        if self.debug: print 'Toggling turn.'
        if self.turn == "white":
            self.turnLabel.config(text="Black player's turn.")
            self.turn = "black"
        else:
            self.turnLabel.config(text="White player's turn.")
            self.turn = "white"
        # Check for skipping turn
        stop = False
        if len(self.validPositions) == 0:
            stop = True
        # Build validPositions
        self.validPositions = []
        for i in range(8):
            for j in range(8):
                if self.validPosition(i, j):
                    self.validPositions.append([i, j])
        print self.validPositions
        # If there are no valid moves, toggle turn.
        if len(self.validPositions) == 0 and stop == False:
            self.toggleTurn()
        elif len(self.validPositions) == 0 and stop == True:
            self.displayWinner()
        self.score()
    # Checks if a position is valid
    def validPosition(self, x, y):
        piece = self.pieces[x][y]
        if piece is None:
            for i in range(-1,2):
                if x+i >= 0 and x+i < 8:
                    for j in range(-1,2):
                        if y+j >= 0 and y+j < 8:
                            nextPiece = self.pieces[x+i][y+j]
                            if nextPiece is not None and self.canvas.gettags(nextPiece)[1] != self.turn:
                                    k = 2
                                    while 0 <= x+(i*k) < 8 and 0<=y+(j*k)<8:
                                        if self.pieces[x+(i*k)][y+(j*k)] is not None and self.canvas.gettags(self.pieces[x+(i*k)][y+(j*k)])[1] == self.turn:
                                            return True
                                        k+=1
        return False

    # Places the piece and reverses appropriate pieces
    def placePieceAndReverseColors(self, x, y):
        # Change in x
        for i in range(-1,2):
                if 0 <= x+i < 8:
                    # Change in y
                    for j in range(-1,2):
                        if 0<=y+j<8:
                            validPath = False
                            k = 1
                            nextPiece = self.pieces[x+(i*k)][y+(j*k)]
                            while nextPiece is not None and self.canvas.gettags(nextPiece)[1] != self.turn and 0 <= x+(i*k) < 8 and 0<=y+(j*k)<8:
                                k+=1
                                if 0 <= x+(i*k) < 8 and 0<=y+(j*k)<8:
                                    nextPiece = self.pieces[x+(i*k)][y+(j*k)]
                                else:
                                    nextPiece = None
                            if nextPiece is not None and self.canvas.gettags(nextPiece)[1] == self.turn:
                                self.pieces[x][y] = self.canvas.create_oval(0,0,0,0,fill=self.turn,tags=("piece",self.turn))
                                for l in range(1,k):
                                    currentPiece = self.pieces[x+(i*l)][y+(j*l)]
                                    self.canvas.delete(currentPiece)
                                    self.pieces[x+(i*l)][y+(j*l)] = None
                                    self.pieces[x+(i*l)][y+(j*l)] = self.canvas.create_oval(0,0,0,0,fill=self.turn,tags=("piece",self.turn))
        self.draw(None)
        return

    def score(self):
        whiteCount = 0
        blackCount = 0
        for x in range(8):
            for y in range(8):
                if self.pieces[x][y] is not None:
                    if self.canvas.gettags(self.pieces[x][y])[1] == "white":
                        whiteCount += 1
                    else:
                        blackCount += 1
        self.whiteScore.config(text="White Score: " + str(whiteCount), relief=SUNKEN)
        self.blackScore.config(text="Black Score: " + str(blackCount), relief=SUNKEN)
        return whiteCount,blackCount

    def displayWinner(self):
        whiteCount, blackCount = self.score()
        if(whiteCount > blackCount):
            tkMessageBox.showinfo("Game Over", "White wins!")
        elif(blackCount > whiteCount):
            tkMessageBox.showinfo("Game Over", "Black wins!")
        else:
            tkMessageBox.showinfo("Game Over", "It's a tie!")

if __name__ == '__main__':
    # Initialize GUI
    root = Tk()
    my_gui = Reversi(root)
    root.aspect(1, 1, 1, 1)  # This doesn't seem to work
    root.mainloop()