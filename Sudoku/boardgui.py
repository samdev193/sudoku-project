import PyQt5.QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QFrame, QPushButton, QMessageBox
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIntValidator
from PyQt5 import uic
from sudoku import solve, is_valid, random_board
import sys
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        uic.loadUi("board.ui",self)
        self.setupUI()


    def setupUI(self):
        self.board =[ [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ]

        # boxes on the board
        self.ltop_box = self.findChild(QFrame, "top_left_frame")
        self.mtop_box = self.findChild(QFrame, "top_middle_frame")
        self.rtop_box = self.findChild(QFrame, "top_right_frame")
        self.lmid_box = self.findChild(QFrame, "middle_left_frame")
        self.mmid_box = self.findChild(QFrame, "middle_middle_frame")
        self.rmid_box = self.findChild(QFrame, "middle_right_frame")
        self.lbot_box = self.findChild(QFrame, "bottom_left_frame")
        self.mbot_box = self.findChild(QFrame, "bottom_middle_frame")
        self.rbot_box = self.findChild(QFrame, "bottom_right_frame")

        # buttons
        self.load_btn = self.findChild(QPushButton, "load_button")
        self.load_btn.clicked.connect(lambda: self.load_board())
        self.clear_btn = self.findChild(QPushButton, "clear_button")
        self.clear_btn.clicked.connect(lambda:self.clear_board())
        self.solve_btn = self.findChild(QPushButton, "solve_button")
        self.solve_btn.clicked.connect(lambda:self.solve_board())

        # holds each column of corresponding rows.
        self.top_row = ({}, {}, {})
        self.mid_row = ({}, {}, {})
        self.bot_row = ({}, {}, {})

        boxes = (self.ltop_box, self.mtop_box, self.rtop_box,
                 self.lmid_box, self.mmid_box, self.rmid_box,
                 self.lbot_box, self.mbot_box, self.rbot_box)


        # populates each row with coordinates of the grid and corresponding line objects
        index = 0
        for i in range(9):
            mychild = boxes[i].findChildren(QLineEdit)

            if i == 3 or i == 6:
                index = 0

            for j in range(9):
                # populates by row instead of box, mirroring 2d list.
                coord = mychild[j].objectName().split('_')
                coord = (int(coord[1]), int(coord[2]))

                if i < 3:
                    self.top_row[index][coord] = mychild[j]

                elif 3 <= i < 6:
                    self.mid_row[index][coord] = mychild[j]

                elif 6 <= i < 9:
                    self.bot_row[index][coord] = mychild[j]
            index += 1


        for i in range(3):
            topkeylist = tuple(self.top_row[i].keys())
            midkeylist = tuple(self.mid_row[i].keys())
            botkeylist = tuple(self.bot_row[i].keys())
            for j in range(9):
                self.top_row[i][topkeylist[j]].installEventFilter(self)
                self.mid_row[i][midkeylist[j]].installEventFilter(self)
                self.bot_row[i][botkeylist[j]].installEventFilter(self)
        self.show()

    # keeps input to only numbers
    def inputvalidaton(self, myline: QLineEdit) -> bool:
        validator = QIntValidator(1,9)
        state = validator.validate(myline.text(),0)[0]
        if state == validator.Acceptable:
            return True
        else:
            myline.setText("")
            return False

    def eventFilter(self, source, event) -> bool:
        for i in range(3):
            topkeylist = tuple(self.top_row[i].keys())
            midkeylist = tuple(self.mid_row[i].keys())
            botkeylist = tuple(self.bot_row[i].keys())


            for j in range(9):

                top_child = self.top_row[i][topkeylist[j]]
                mid_child = self.mid_row[i][midkeylist[j]]
                bot_child = self.bot_row[i][botkeylist[j]]

                # checks if input is valid and box on board selected
                if source == top_child and event.type() == QEvent.KeyRelease and self.inputvalidaton(source):
                    self.check_valid(source, self.top_row[i])

                elif source == mid_child and event.type() == QEvent.KeyRelease and self.inputvalidaton(source):
                    self.check_valid(source, self.mid_row[i])

                elif source == bot_child and event.type() == QEvent.KeyRelease and self.inputvalidaton(source):
                    self.check_valid(source, self.bot_row[i])

        return super().eventFilter(source ,event)

    # checks if input does not violate sudoku rules
    def check_valid(self, source, row: dict):
        for key, value in row.items():
            if value == source:
                target = (key[0], key[1])
                if not is_valid(self.board, (target), int(source.text())):
                    source.setText("")
                else:
                    source.setStyleSheet("color:red")
                    self.board[target[0]][target[1]] = int(source.text())
                    self.check_win()

    # checks if board has been solved yet
    def check_win(self) -> bool:
            for i in range(len(self.board)):
                for j in range(len(self.board)):
                    if self.board[i][j] == 0:
                        return False
            self.show_popup("You've solved the puzzle!")
            self.clear_board()

    def show_popup(self, text, icon=None):
        msg = QMessageBox()
        msg.setWindowTitle("Sudoku")
        msg.setText(text + "\t\t")

        if icon != None:
            msg.setIcon(icon)
        x = msg.exec_()

    def solve_board(self):
        if not solve(self.board):
            self.show_popup("This board is unsolvable!", QMessageBox.Critical)
            self.clear_board()
        else:
            for i in range(len(self.board)):

                count = 0 # tracks when to iterate through keylist

                for j in range(len(self.board)):
                    # top_row row
                    top_child = self.top_row[count].get((i, j))
                    # middle row
                    mid_child = self.mid_row[count].get((i, j))
                    # bottom row
                    bot_child = self.bot_row[count].get((i, j))

                    # iterates by row through each box
                    if j % 3 == 0 and j != 0:
                        count += 1

                        # end of row has been reached
                        if count == 3:
                            break
                        top_child = self.top_row[count].get((i, j))
                        mid_child = self.mid_row[count].get((i, j))
                        bot_child = self.bot_row[count].get((i, j))

                    target_child = (top_child or mid_child or bot_child)

                    # fills in boxes on board
                    if not target_child.isReadOnly():
                        target_child.setStyleSheet("color:red")
                    target_child.setText(str(self.board[i][j]))
                    target_child.setReadOnly(True)

            self.show_popup("Game over!")
    def load_board(self):
        self.clear_board()
        # generates a random board
        random_board(self.board)

        # populates board
        for i in range(len(self.board)):

            count = 0 # tracks when to iterate through keylist

            for j in range(len(self.board)):
                # top_row row
                top_child = self.top_row[count].get((i, j))
                # middle row
                mid_child = self.mid_row[count].get((i, j))
                # bottom row
                bot_child = self.bot_row[count].get((i, j))

                # iterates by row through each box
                if j % 3 == 0 and j != 0:
                    count += 1

                    # end of row has been reached
                    if count == 3:
                        break
                    top_child = self.top_row[count].get((i, j))
                    mid_child = self.mid_row[count].get((i, j))
                    bot_child = self.bot_row[count].get((i, j))

                target_child = (top_child or mid_child or bot_child)

                if self.board[i][j] == 0:
                    target_child.setText('')

                else:
                    # fills in boxes on board
                    target_child.setStyleSheet("color:black")
                    target_child.setText(str(self.board[i][j]))
                    target_child.setReadOnly(True)


    def clear_board(self):
        # add a pop up message to this

        for i in range(len(self.board)):

            count = 0 # tracks when to iterate through keylist


            for j in range(len(self.board)):
                # top_row row
                top_child = self.top_row[count].get((i, j))
                # middle row
                mid_child = self.mid_row[count].get((i, j))
                # bottom row
                bot_child = self.bot_row[count].get((i, j))

                if j % 3 == 0 and j != 0:
                    count += 1
                    if count == 3:
                        break
                    top_child = self.top_row[count].get((i, j))
                    mid_child = self.mid_row[count].get((i, j))
                    bot_child = self.bot_row[count].get((i, j))

                # clears boxes on board.
                target_child = (top_child or mid_child or bot_child)
                target_child.setText('')
                target_child.setStyleSheet("color:black")
                target_child.setReadOnly(False)
                self.board[i][j] = 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()