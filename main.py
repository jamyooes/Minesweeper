# James Yoo

import sys
import time
import random

# import pyqt stuff
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPainter , QBrush, QColor, QImage, QPixmap, QPen
from PyQt5.QtCore import QSize, pyqtSignal, QTimer
from PyQt5.QtWidgets import QMessageBox


# global variables to hold positions
bombs = [] # this global list will store the locations of the mines
# GAME STATES, will use for conditions to control the timer, and wins
READY = 0
GAMEOVER = 1
WIN = 2
PLAYING = 3

class MineSweeperUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # set title and size when intialized
        self.setWindowTitle("Scuffed Minesweeper")
        # stores game widgets and removes them when the user decides to change modes
        self.games = []        
        # a home screen
        self.Home()
    
    # home screen
    def Home(self):
        # Home screen Widget and central widget
        self.current_screen = QWidget()
        self.setCentralWidget(self.current_screen)

        # Layout for the current_screen
        self.layout = QHBoxLayout()

        # Play Widget
        play_widget = PlayWidget(self)

        # set the layout for the main menu
        self.current_screen.setLayout(self.layout)

    # easy difficulty when selected, sets the dimensions and the number of mines
    def PlayEasy(self):
        self.gameLength = 9
        self.gameWidth = 9
        self.mines = 10
        play = PlayPage(self)
        # remove previous board when starting a new game
        if len(self.games) == 1:
            for i in (range(self.layout.count())): 
                if self.layout.itemAt(i).widget() == self.games[0]:
                    self.layout.itemAt(i).widget().setParent(None)
            self.games.pop(0)
        self.games.append(play)
        self.layout.addWidget(play)
    
    # medium difficulty when selected, sets the dimensions and the number of mines
    def PlayMedium(self):
        self.gameLength = 16
        self.gameWidth = 16
        self.mines = 40
        play = PlayPage(self)
        # remove previous board when starting a new game
        if len(self.games) == 1:
            for i in (range(self.layout.count())): 
                if self.layout.itemAt(i).widget() == self.games[0]:
                    self.layout.itemAt(i).widget().setParent(None)
            self.games.pop(0)
        self.games.append(play)
        self.layout.addWidget(play)

    # Hard difficulty when selected, sets the dimensions and the number of mines
    def PlayHard(self):
        self.gameLength = 16
        self.gameWidth = 30
        self.mines = 99
        play = PlayPage(self)
        # remove previous board when starting a new game
        if len(self.games) == 1:
            for i in (range(self.layout.count())): 
                if self.layout.itemAt(i).widget() == self.games[0]:
                    self.layout.itemAt(i).widget().setParent(None)
            self.games.pop(0)
        self.games.append(play)
        self.layout.addWidget(play)
    
    def Controls(self):
        controls = ControlsPage(self)
        self.layout.addWidget(controls)
        self.setCentralWidget(controls)


# Play Widgets (easy, medium, hard)
class PlayWidget(QWidget):
    def __init__(self, parent=None):
        super(PlayWidget, self).__init__(parent)
        # options for user to select a level
        self.easy = QPushButton('Play 9X9 Minsweeper')
        self.medium = QPushButton('Play 16X16 Minesweeper')
        self.hard = QPushButton('Play 30X16 Minesweeper')
        self.controls = QPushButton('Controls')

        # add widget to screen
        parent.layout.addWidget(self.easy)
        parent.layout.addWidget(self.medium)
        parent.layout.addWidget(self.hard)
        parent.layout.addWidget(self.controls)


        # when clicked set up game
        self.easy.clicked.connect(self.parent().PlayEasy) 
        self.medium.clicked.connect(self.parent().PlayMedium) 
        self.hard.clicked.connect(self.parent().PlayHard) 
        self.controls.clicked.connect(self.parent().Controls)

# Controls/Manual
class ControlsPage(QWidget):
    def __init__(self, parent = None):
        super(ControlsPage, self).__init__(parent)
        layout = QVBoxLayout()
        self.control_title = QLabel('Controls')
        self.control_left = QLabel('Left Mouse Button Click to reveal tiles')
        self.control_right = QLabel('Right Mouse Button Click to set flags. You can only remove flags by right clicking them again')
        self.control_smile = QLabel('Click on the smiley to start a new game')
        self.how_to = QLabel ("You win if you can clear all tiles that are not mines")

        layout.addWidget(self.control_title)
        layout.addWidget(self.control_left)
        layout.addWidget(self.control_right)
        layout.addWidget(self.how_to)
        layout.addStretch()

        self.button = QPushButton('Home')
        self.button.clicked.connect(self.parent().Home) 
        layout.addWidget(self.button)

        self.setLayout(layout)

# Game Screen
class PlayPage(QMainWindow):

    def __init__(self, parent=None):
        super(PlayPage, self).__init__(parent)
        # basic details about the mines and board size
        self.mines = parent.mines 
        self.gameLength = parent.gameLength
        self.gameWidth = parent.gameWidth

        layout = QHBoxLayout()
        window = QWidget()

        # label for the remaining mines
        self.totalMines = QLabel(str(self.mines))  
        self.totalMines.setAlignment(Qt.AlignCenter)
        
        # label for setting the clock to minesweeper
        self.timeDisplay = QLabel("000")
        self.timeDisplay.setAlignment(Qt.AlignCenter)

        # set up the timer
        self.gameTimer = QTimer()
        self.gameTimer.timeout.connect(self.updateTime)
        self.gameTimer.start(1000)  # update timer by 1 second

        # button widget to reset the board, also use an image for the reset button minesweeper uses the face
        self.reset = QPushButton()
        self.reset.setFixedSize(QSize(48, 48))
        self.reset.setStyleSheet("border-image : url(./images/smileyReset.png)")
        self.reset.pressed.connect(self.resetState)

        # basic fonts to make the font look bigger
        fontMenu = QFont('Arial', 24)
        self.totalMines.setFont(fontMenu)
        self.timeDisplay.setFont(fontMenu)

        # images for the UI
        mineImg = QLabel()
        mineImg.setFixedSize(QSize(32, 32))
        mineImg.setStyleSheet("border-image : url(./images/mine.png)")

        # add top part of the menu and widget to the layout
        layout.addWidget(mineImg)
        layout.addWidget(self.totalMines)
        layout.addWidget(self.reset)
        layout.addWidget(self.timeDisplay)

        # horizontal box layout storing the entire screen for the game
        screen = QVBoxLayout()
        screen.addLayout(layout)

        # grid for the game
        self.grid = QGridLayout()
        self.grid.setSpacing(5)

        screen.addLayout(self.grid)

        # set the layout
        window.setLayout(screen)
        self.setCentralWidget(window)

        # initialize the map
        self.initMap()
        self.gameState(READY)

        # start the state of the map in a new game, and the timer wont start until clicking
        self.resetMap()
        self.gameState(READY)

    # game set up
    def initMap(self):
        for row in range (0, self.gameLength):
            for col in range (0, self.gameWidth):
                cell = MinesweeperCell(row, col)
                # add the cell into the board
                self.grid.addWidget(cell, row, col)
                # configure all the cell's behavior to the board's method
                # for example clicking on a mine, wiil trigger the board's gameover method 
                cell.gameIsOver.connect(self.gameOver)
                cell.clicks.connect(self.gameStart)
                cell.expand.connect(self.expandMap)
                
    # the logic is to check all the cells around the current cell
    # if the tile is not a mine then it will reveal it and then do another 
    # call to this function from click() and check again
    def expandMap(self, cellX, cellY):
        # max and min are border checks to prevent going out of bounds
        for adjacentX in range(max(0, cellX - 1), min(cellX + 2, self.gameLength)):
            for adjacentY in range(max(0, cellY - 1), min(cellY + 2, self.gameWidth)):
                adjacentCell = self.grid.itemAtPosition(adjacentX, adjacentY).widget()
                if not adjacentCell.mine_flag:
                    adjacentCell.clickedTile()

    # reset the map or start the state of the map in the case of a new game
    def resetMap(self):

        for row in range(0, self.gameLength):
            for col in range(0, self.gameWidth):
                cell = self.grid.itemAtPosition(row, col).widget()
                cell.reset()
        
        bombLocations = []
        while len(bombLocations) < self.mines:
            bombRow = random.randint(0, self.gameLength - 1)
            bombCol = random.randint(0, self.gameWidth - 1)
            if (bombRow, bombCol) not in bombLocations:
                cell = self.grid.itemAtPosition(bombRow, bombCol).widget()
                cell.mine_flag = True 
                bombLocations.append((bombRow, bombCol))

        # triple for loops was very hard to read 
        def adjacentInCell(row, col):
            curr = self.getAdjacents(row, col)
            minesAdjacent = 0
            for bombs in curr:
                if bombs.mine_flag:
                    minesAdjacent += 1

            return minesAdjacent

        for row in range (0, self.gameLength):
            for col in range (0, self.gameWidth):
                cell = self.grid.itemAtPosition(row, col).widget()
                cell.adjacent = adjacentInCell(row, col) 
        

        
    def getAdjacents(self, row, col):
        adjacencies = []
        for cellAdjacentX in range(max(0, row - 1), min(row + 2, self.gameLength)):
            for cellAdjacentY in range(max(0, col - 1), min(col + 2, self.gameWidth)):
                adjacencies.append(self.grid.itemAtPosition(cellAdjacentX, cellAdjacentY).widget())

        return adjacencies

    def gameState(self, state):
        self.state = state

    def gameStart(self):
        # start the timer on the first click on the grid
        if self.state != PLAYING:
            self.gameState(PLAYING)
            self.timeStart = int(time.time())
        self.remainingBombsUpdate()
        self.checkWin()
        
    # reveal the map when the game was over
    def gameOver(self):
        self.revealMap()
        self.gameState(GAMEOVER)
        self.popUp()


    def revealMap(self):
        for row in range(0, self.gameLength):
            for col in range(0, self.gameWidth):
                cell = self.grid.itemAtPosition(row, col).widget()
                cell.reveal()    

    def updateTime(self):
        if self.state == PLAYING:
            elapsed = int (time.time()) - self.timeStart
            self.timeDisplay.setText(str(elapsed))

    # reset the state for the new game
    def resetState(self):
        if self.state == PLAYING:
            self.gameState(GAMEOVER)
            self.revealMap()

        elif self.state == GAMEOVER or self.state == WIN:
            self.gameState(READY)
            self.resetMap()
    
    # this method will check if the user won, which will stop the timer and reveal all the bombs
    def checkWin(self):
        if self.state != READY or self.state != GAMEOVER:
            for row in range(self.gameLength):
                for col in range(self.gameWidth):
                    cell = self.grid.itemAtPosition(row, col).widget()
                    # if the cells have not all been found then the game is not over
                    if not cell.revealed and cell.mine_flag == False :
                        return False
                    # this is a guard case 
                    elif cell.revealed and cell.mine_flag == True:
                        return False
            self.state = WIN
            self.popUp()
            self.revealMap()
            return True
    
    # this method will update the remaining bombs based on flags, does not gaurentee if there is indeed that many bombs but helps user this is a feature from minesweeper
    def remainingBombsUpdate(self):
        markedMines = 0 # this will be used to update the remaining bombs
        for row in range(self.gameLength):
            for col in range(self.gameWidth):
                cell = self.grid.itemAtPosition(row, col).widget()
                if cell.flagged == True:
                    markedMines += 1
        self.totalMines.setText(str(self.mines-markedMines))

    # pop up when user wins or loses
    def popUp(self):
        if self.state == GAMEOVER:
            msg = QMessageBox()
            msg.setWindowTitle("LOST")
            msg.setText("Better luck next time :p")
            x = msg.exec_()
        elif self.state == WIN:
            msg = QMessageBox()
            msg.setWindowTitle("WINNER")
            msg.setText("WINNER!!!!")
            x = msg.exec_()
# GAME Cell
class MinesweeperCell(QWidget):
    # need to connect to the parent class's methods on the board from the cell
    # technically i can do self.parent().parent().whatevermethod() but this seems more annoying
    gameIsOver = pyqtSignal()
    clicks = pyqtSignal()
    expand = pyqtSignal(int, int)

    def __init__(self, row, col):
        super(MinesweeperCell, self).__init__()
        self.row = row 
        self.col = col
        self.setFixedSize(QSize(20, 20))
        
        # bomb img 
        self.mineImg = QImage("./images/mine.png")
        self.flagImg = QImage("./images/flag.png")

    
    # reset all flags when resetting the game
    def reset(self):
        self.mine_flag = False # bool variable used to check if there's a mine
        self.adjacent = 0 # int variable to check for adjacent bombs
        self.flagged = False # flagged bool variable to show if a tile is flagged
        self.revealed = False # revealed bool variable to check if a tile has been revealed
        self.update() # updates the view 

    # method override pyqt's paintEvent, which will also update when calling self.update()
    # the goal of this function is to draw the tiles on the grid
    def paintEvent(self, cells):
        #sets up class to draw on widgets
        paint = QPainter(self)

        # this is pyqt's way of getting the dimensions to the widget to be drawn
        cell = cells.rect()

        # if the cell is revealed then change the color of the tile
        # set the color in revealed cells to a blueish - turquoish color
        if self.revealed:
            inner = QColor(75, 190, 175)
        # this is for untouched tiles on the grid, which will just be gray
        else: 
            inner = Qt.lightGray
        # fill the tile with their color
        paint.fillRect(cell, QBrush(inner))
        # draw the cell on the grid with the newly painted color
        paint.drawRect(cell)

        if self.revealed:
            # set the image of the mine when revealed
            if self.mine_flag: 
                paint.drawPixmap(cell, QPixmap(self.mineImg))
            # set the numeric value when revealing the cell that are adjacent to mine
            elif self.adjacent > 0:
                pen = QPen(QColor("#000000"))
                paint.setPen(pen)
                # center the text on the tile 
                paint.drawText(cell, Qt.AlignCenter, str(self.adjacent))
        # put the image of the flag on the cell when flagged
        elif self.flagged: 
                paint.drawPixmap(cell, QPixmap(self.flagImg))

    # flag method to update when flagging a cell
    def flag(self):
        self.flagged = not self.flagged
        self.update()
        self.clicks.emit()

    # reveal method to show that a cell is revealed
    def reveal(self):
        self.flagged = False
        self.revealed = True
        self.update()

    # when clicking on a non-revealed tile then reveal the tile 
    # in the case that the tile is empty then reveal all the tiles that are empty and connected
    def clickedTile(self):
        if not self.revealed:
            self.reveal()
            if self.adjacent == 0:
                self.expand.emit(self.row, self.col)
        # this will trigger a call to the parent class to check if the user won and the flags placed
        self.clicks.emit()

    # react to the user's clicks on a cell
    def mouseReleaseEvent(self, user_click):
        # if the user right clicks then apply a flag
        if (user_click.button() == Qt.RightButton and not self.revealed):
            self.flag()
        # if the user left clicks then open the tile
        elif (user_click.button() == Qt.LeftButton):
            # if the user clicks on a flag nothing happens
            if self.flagged:
                return
            # check the tile the user clicked
            self.clickedTile()
            # if the user clicked on a mine then game is over
            if self.mine_flag:
                self.gameIsOver.emit()

def main():
    # instance of class
    mineInstance = QApplication(sys.argv)
    #view 
    view = MineSweeperUI()
    view.show()
    #main event loop
    sys.exit(mineInstance.exec())


if __name__ == "__main__":
    main()