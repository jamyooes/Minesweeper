# James Yoo

import sys

# import pyqt stuff
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

class MineSweeperUI(QMainWindow):
    def __init__(self):
        super().__init__()
        # set title and size when intialized
        self.setWindowTitle("Scuffed Minesweeper")
        self.setFixedSize(700,700)
        
        # a home screen
        self.Home()
    
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

    # easy difficulty when selected
    def PlayEasy(self):
        self.gameLength = 9
        self.gameWidth = 9
        self.mines = 10
        play = PlayPage(self)
        self.layout.addWidget(play)
        self.setCentralWidget(play)
    
    # medium difficulty when selected
    def PlayMedium(self):
        self.gameLength = 16
        self.gameWidth = 16
        self.mines = 40
        play = PlayPage(self)
        self.layout.addWidget(play)
        self.setCentralWidget(play)

    # Hard difficulty when selected
    def PlayHard(self):
        self.gameLength = 16
        self.gameWidth = 30
        self.mines = 99
        play = PlayPage(self)
        self.layout.addWidget(play)
        self.setCentralWidget(play)

# Play Widget
class PlayWidget(QWidget):
    def __init__(self, parent=None):
        super(PlayWidget, self).__init__(parent)
        # options for user to select a level
        self.easy = QPushButton('Play 9X9 Minsweeper')
        self.medium = QPushButton('Play 16X16 Minesweeper')
        self.hard = QPushButton('Play 30X16 Minesweeper')

        # add widget to screen
        parent.layout.addWidget(self.easy)
        parent.layout.addWidget(self.medium)
        parent.layout.addWidget(self.hard)

        # when clicked set up game
        self.easy.clicked.connect(self.parent().PlayEasy) 
        self.medium.clicked.connect(self.parent().PlayMedium) 
        self.hard.clicked.connect(self.parent().PlayHard) 


# Filler Screen will become game logic
class PlayPage(QWidget):
    def __init__(self, parent=None):
        super(PlayPage, self).__init__(parent)
        # basic details about the mines and board size
        self.mines = parent.mines 
        self.gameLength = parent.gameLength
        self.gameWidth = parent.gameWidth

        layout = QHBoxLayout()
        window = QWidget()

        # label for the remaining mines
        self.totalMines = QLabel()
        self.totalMines.setAlignment(Qt.AlignCenter)
        
        self.totalMines.setText("mines")

        layout.addWidget(self.totalMines)

        
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