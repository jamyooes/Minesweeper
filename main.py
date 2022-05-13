# James Yoo

import sys

# import pyqt stuff
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget

class MineSweeperUI(QMainWindow):
    pass

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