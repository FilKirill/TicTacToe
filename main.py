import sys
import random

from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtGui import QPixmap, QBrush, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QHeaderView, QFileDialog, \
    QGridLayout, QWidget, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy, QHBoxLayout, QLabel


class GameModeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 442)
        self.setWindowTitle("Главное меню")
        self.background = 'fon.jpg'
        self.layout = QVBoxLayout()

        self.layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.btn_ai = QPushButton("Играть против компьютера")
        self.btn_ai.setFixedSize(270, 40)
        self.btn_ai.clicked.connect(self.start_ai_game)
        self.btn_ai.setStyleSheet("background-color: white; color: blue; font-size: 20px;")

        self.btn_2 = QPushButton("Два Игрока")
        self.btn_2.setFixedSize(270, 40)
        self.btn_2.clicked.connect(self.start_2_game)
        self.btn_2.setStyleSheet("background-color: white; color: blue; font-size: 20px;")

        self.ex = QPushButton("Выйти")
        self.ex.setFixedSize(270, 40)
        self.ex.clicked.connect(self.ext)
        self.ex.setStyleSheet("background-color: white; color: blue; font-size: 20px;")

        self.layout.addWidget(self.btn_ai, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.btn_2, alignment=Qt.AlignCenter)
        self.layout.addWidget(self.ex, alignment=Qt.AlignCenter)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.background)
        painter.drawPixmap(self.rect(), pixmap)

    def start_ai_game(self):
        self.w2 = TicTacToe()
        self.w2.show()
        self.close()

    def ext(self):
        self.close()

    def start_2_game(self):
        self.w2 = TicTacToe2()
        self.w2.show()
        self.close()


class TicTacToe2(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 442)
        self.setWindowTitle("Крестики-нолики")
        self.background = 'game2.jpg'
        self.player_score = 0
        self.ai_score = 0
        self.current_player = None
        self.initUI()
        QTimer.singleShot(0, self.rand)

    def initUI(self):
        self.buttons = []
        main_layout = QVBoxLayout()
        grid = QGridLayout()
        for i in range(3):
            self.buttons.append([])
            for j in range(3):
                button = QPushButton(' ')
                button.setFixedSize(107, 107)
                button.clicked.connect(self.buttonClicked)
                button.setStyleSheet("font-size: 24px;")
                grid.addWidget(button, i, j)
                self.buttons[i].append(button)

        main_layout.addLayout(grid)
        layout = QHBoxLayout()
        restart_button = QPushButton('Начать заново')
        restart_button.setFixedSize(150, 50)
        restart_button.clicked.connect(self.restartGame)
        restart_button.setStyleSheet("background-color: white; color: blue; font-size: 18px;")

        back_button = QPushButton('Главное меню')
        back_button.setFixedSize(150, 50)
        back_button.clicked.connect(self.back_main)
        back_button.setStyleSheet("background-color: white; color: blue; font-size: 18px;")

        self.player_label = QLabel(f'{self.player_score}', self)
        self.player_label.setStyleSheet("font-size: 45px; font-weight: bold; color: red;")
        self.player_label.setFixedSize(100, 100)
        self.player_label.move(50, 250)
        self.player_label.adjustSize()

        self.ai_label = QLabel(f'{self.ai_score}', self)
        self.ai_label.setStyleSheet("font-size: 45px; font-weight: bold; color: blue;")
        self.ai_label.setFixedSize(100, 100)
        self.ai_label.move(505, 250)
        self.ai_label.adjustSize()

        layout.addWidget(restart_button, alignment=Qt.AlignCenter)
        layout.addWidget(back_button, alignment=Qt.AlignCenter)
        main_layout.addLayout(layout)
        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)

    def rand(self):
        self.current_player = random.choice(['X', 'O'])
        if self.current_player == "O":
            self.result(f"Игрок 2 начинает первым!")
        else:
            self.result(f"Игрок 1 начинает первым!")

    def result(self, message):
        QMessageBox.information(self, "Результат жеребьёвки", message)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.background)
        painter.drawPixmap(self.rect(), pixmap)

    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == ' ':
            sender.setText(self.current_player)
            sender.setStyleSheet(
                f"font-size: 32px; font-weight: bold; color: {'red' if self.current_player == 'X' else 'blue'};")
            if not self.checkWin(self.current_player):
                self.switchPlayer()

    def switchPlayer(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def checkWin(self, player):
        for i in range(3):
            if self.buttons[i][0].text() == self.buttons[i][1].text() == self.buttons[i][2].text() == player:
                self.gameOver(player)
                return True
            if self.buttons[0][i].text() == self.buttons[1][i].text() == self.buttons[2][i].text() == player:
                self.gameOver(player)
                return True
        if self.buttons[0][0].text() == self.buttons[1][1].text() == self.buttons[2][2].text() == player:
            self.gameOver(player)
            return True
        if self.buttons[0][2].text() == self.buttons[1][1].text() == self.buttons[2][0].text() == player:
            self.gameOver(player)
            return True
        return False

    def gameOver(self, player):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setEnabled(False)
        if player == "X":
            question = QMessageBox()
            question.setWindowTitle('Игра окончена')
            question.setText(f'Игрок 1 выиграл!')
            question.setIcon(QMessageBox.Information)
            question.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            question.exec_()
        else:
            question = QMessageBox()
            question.setWindowTitle('Игра окончена')
            question.setText(f'Игрок 2 выиграл!')
            question.setIcon(QMessageBox.Information)
            question.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            question.exec_()
        if player == "X":
            self.player_score += 1
        else:
            self.ai_score += 1
        self.updateScore()

    def updateScore(self):
        self.player_label.setText(f'{self.player_score}')
        self.ai_label.setText(f'{self.ai_score}')

    def restartGame(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setText(' ')
                self.buttons[i][j].setEnabled(True)
                self.buttons[i][j].setStyleSheet("font-size: 24px;")
        QTimer.singleShot(0, self.rand)

    def back_main(self):
        self.w2 = GameModeWindow()
        self.w2.show()
        self.close()


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 442)
        self.background_image_path = 'game.jpg'
        self.current_player = None
        self.player_score = 0
        self.ai_score = 0
        self.initUI()

    def initUI(self):
        self.buttons = []
        main_layout = QVBoxLayout()
        self.setWindowTitle("Крестики-нолики")
        grid = QGridLayout()

        for i in range(3):
            self.buttons.append([])
            for j in range(3):
                button = QPushButton(' ')
                button.setFixedSize(107, 107)
                button.clicked.connect(self.buttonClicked)
                button.setStyleSheet("font-size: 24px;")
                grid.addWidget(button, i, j)
                self.buttons[i].append(button)

        main_layout.addLayout(grid)
        button_layout = QHBoxLayout()
        restart_button = QPushButton('Начать заново')
        restart_button.setFixedSize(150, 50)
        restart_button.clicked.connect(self.restartGame)
        restart_button.setStyleSheet("background-color: white; color: blue; font-size: 18px;")

        back_button = QPushButton('Главное меню')
        back_button.setFixedSize(150, 50)
        back_button.clicked.connect(self.back_main)
        back_button.setStyleSheet("background-color: white; color: blue; font-size: 18px;")

        button_layout.addWidget(restart_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(back_button, alignment=Qt.AlignCenter)
        main_layout.addLayout(button_layout)

        self.player_label = QLabel(f'{self.player_score}', self)
        self.player_label.setStyleSheet("font-size: 45px; font-weight: bold; color: red;")
        self.player_label.setFixedSize(100, 100)
        self.player_label.move(50, 250)
        self.player_label.adjustSize()

        self.ai_label = QLabel(f'{self.ai_score}', self)
        self.ai_label.setStyleSheet("font-size: 45px; font-weight: bold; color: blue;")
        self.ai_label.setFixedSize(100, 100)
        self.ai_label.move(505, 250)
        self.ai_label.adjustSize()

        main_layout.setAlignment(Qt.AlignCenter)
        self.setLayout(main_layout)
        QTimer.singleShot(0, self.rand)

    def rand(self):
        self.current_player = random.choice(["X", "O"])
        if self.current_player == "O":
            self.result("Компьютер ходит первым!")
            self.aiMove()
        else:
            self.result("Вы ходите первым!")

    def result(self, message):
        QMessageBox.information(self, "Результат жеребьёвки", message)

    def paintEvent(self, event):
        painter = QPainter(self)
        pixmap = QPixmap(self.background_image_path)
        painter.drawPixmap(self.rect(), pixmap)

    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == ' ' and self.current_player == "X":
            sender.setText('X')
            sender.setStyleSheet("font-size: 45px; font-weight: bold; color: red;")
            if not self.checkWin('X'):
                self.current_player = "O"
                self.aiMove()

    def aiMove(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3) if self.buttons[i][j].text() == ' ']
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.buttons[i][j].setText('O')
            self.buttons[i][j].setStyleSheet("font-size: 45px; font-weight: bold; color: blue;")
            if not self.checkWin('O'):
                self.current_player = "X"

    def checkWin(self, player):
        for i in range(3):
            if self.buttons[i][0].text() == self.buttons[i][1].text() == self.buttons[i][2].text() == player:
                self.gameOver(player)
                return True
            if self.buttons[0][i].text() == self.buttons[1][i].text() == self.buttons[2][i].text() == player:
                self.gameOver(player)
                return True
        if self.buttons[0][0].text() == self.buttons[1][1].text() == self.buttons[2][2].text() == player:
            self.gameOver(player)
            return True
        if self.buttons[0][2].text() == self.buttons[1][1].text() == self.buttons[2][0].text() == player:
            self.gameOver(player)
            return True
        return False

    def gameOver(self, player):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setEnabled(False)
        if player == "X":
            question = QMessageBox()
            question.setWindowTitle('Игра окончена')
            question.setText(f'Вы выиграли!')
            question.setIcon(QMessageBox.Information)
            question.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            question.exec_()
        else:
            question = QMessageBox()
            question.setWindowTitle('Игра окончена')
            question.setText(f'Компьютер выиграл!')
            question.setIcon(QMessageBox.Information)
            question.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            question.exec_()
        if player == "X":
            self.player_score += 1
        else:
            self.ai_score += 1
        self.updateScore()

    def updateScore(self):
        self.player_label.setText(f'{self.player_score}')
        self.ai_label.setText(f'{self.ai_score}')

    def restartGame(self):
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].setText(' ')
                self.buttons[i][j].setEnabled(True)
                self.buttons[i][j].setStyleSheet("font-size: 24px;")
        self.rand()

    def back_main(self):
        self.w2 = GameModeWindow()
        self.w2.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GameModeWindow()
    window.show()
    sys.exit(app.exec_())
