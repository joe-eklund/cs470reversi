from Tkinter import *


class Reversi:
    board = []
    pieces = []
    previewPiece = None
    turn = "white"

    def __init__(self, master):
        # Initialize window
        self.master = master
        master.title("Reversi")

        # New game button
        self.greet_button = Button(master, text="Start New Game", command=self.initializeBoard)
        self.greet_button.pack()

        # Turn Label
        self.turnLabel = Label(master, text="")
        self.turnLabel.pack()

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
        self.turn = "white"
        self.pieces = [[None for x in range(8)] for y in range(8)]
        self.pieces[3][3] = self.canvas.create_oval(0, 0, 0, 0, fill="white")
        self.pieces[3][4] = self.canvas.create_oval(0, 0, 0, 0, fill="black")
        self.pieces[4][3] = self.canvas.create_oval(0, 0, 0, 0, fill="black")
        self.pieces[4][4] = self.canvas.create_oval(0, 0, 0, 0, fill="white")
        self.toggleTurn()
        self.draw(None)

    # Redraw the board
    def draw(self, event):
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
        piece = self.pieces[x][y]  # Piece may be null(None)
        if True:  # to do: (if valid move toggle turn and reverse pieces)
            self.toggleTurn()

    # fires when the mouse enters a square of the board
    def onEnter(self, event):
        x, y = self.getBoardPos(event.x, event.y)
        square = self.board[x][y]
        piece = self.pieces[x][y]  # Piece may be null(None)
        color = "gray"
        if self.turn == "black":
            color = "gray20"
        self.canvas.delete(self.previewPiece)
        self.previewPiece = self.canvas.create_oval(self.canvas.coords(square), fill=color)
        self.canvas.tag_bind(self.previewPiece, "<Button-1>", self.selectPosition)

    # fires when the mouse leaves a square of the board
    def onLeave(self, event):
        x, y = self.getBoardPos(event.x, event.y)
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
        if self.turn == "white":
            self.canvas.tag_unbind("white", "<Button-1>")
            self.turnLabel.config(text="Black player's turn.")
            self.turn = "black"
        else:
            self.canvas.tag_unbind("black", "<Button-1>")
            self.turnLabel.config(text="White player's turn.")
            self.turn = "white"

if __name__ == '__main__':
    # Initialize GUI
    root = Tk()
    my_gui = Reversi(root)
    root.aspect(1, 1, 1, 1)  # This doesn't seem to work
    root.mainloop()