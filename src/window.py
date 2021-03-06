'''
Created on 4 Mar 2016

@author: Martin Vidjeskog
'''


import sys
from PyQt5 import QtGui, QtWidgets
from src.buttonActions import ButtonListener
from src.keyActions import KeyListener


class GameWindow(QtWidgets.QWidget):

    def __init__(self):
        '''Constructor'''
        super(GameWindow, self).__init__()
        self.__initView()
        self.maze = None
        self.player = None
        self.demo = None
        self.state = 0
        self.buttonListener = ButtonListener(self)
        self.keyListener = KeyListener(self)

    def __initView(self):
        ''' create window '''
        self.setFixedSize(825, 700)
        self.setAutoFillBackground(True)
        self.setUpdatesEnabled(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QtGui.QColor("#808080"))
        self.setPalette(p)
        self.setWindowTitle("Labyrintti V.0.3.0")
        qr = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        ''' create text field '''
        self.textbox = QtWidgets.QTextEdit(self)
        self.textbox.setReadOnly(True)
        self.textbox.move(50, 551)
        self.textbox.resize(725, 125)
        self.textbox.setText("Tervetuloa Labyrintti-pelin pariin.")

        ''' create button for generating a labyrint '''
        self.genButton = QtWidgets.QPushButton("Generoi Labyrintti", self)
        self.genButton.resize(200, 50)
        self.genButton.move(50, 25)
        self.genButton.clicked.connect(lambda: self.buttonClicked())

        ''' create button for loading a labyrint '''
        self.loadButton = QtWidgets.QPushButton("Lataa Labyrintti", self)
        self.loadButton.resize(200, 50)
        self.loadButton.move(50, 100)
        self.loadButton.clicked.connect(lambda: self.buttonClicked())

        ''' create button for saving a labyrint '''
        self.saveButton = QtWidgets.QPushButton("Tallenna Labyrintti", self)
        self.saveButton.resize(200, 50)
        self.saveButton.move(50, 175)
        self.saveButton.clicked.connect(lambda: self.buttonClicked())

        ''' create button for starting a game '''
        self.playButton = QtWidgets.QPushButton("Pelaa", self)
        self.playButton.resize(200, 50)
        self.playButton.move(50, 250)
        self.playButton.clicked.connect(lambda: self.buttonClicked())

        ''' create button for showing a demo solution '''
        self.demoButton = QtWidgets.QPushButton(
            "Luovuta ja anna ratkaisu", self)
        self.demoButton.resize(200, 50)
        self.demoButton.move(50, 325)
        self.demoButton.clicked.connect(lambda: self.buttonClicked())

        ''' create button to show information about the program '''
        self.infoButton = QtWidgets.QPushButton("Tietoja ohjelmasta", self)
        self.infoButton.clicked.connect(lambda: self.buttonClicked())
        self.infoButton.resize(200, 50)
        self.infoButton.move(50, 401)

        ''' create button to exit the program '''
        self.exitButton = QtWidgets.QPushButton("Lopeta", self)
        self.exitButton.clicked.connect(lambda: self.buttonClicked())
        self.exitButton.resize(200, 50)
        self.exitButton.move(50, 476)

        ''' title for settings menu '''
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(14)
        self.label1 = QtWidgets.QLabel("Valitse labyrintin tyyppi", self)
        self.label1.setFont(font)
        self.label1.move(290, 40)
        self.label1.setVisible(False)

        ''' initialize settings menu '''
        self.checkBox1 = QtWidgets.QCheckBox("Tavallinen 2DLabyrintti", self)
        self.checkBox1.move(300, 70)
        self.checkBox1.setVisible(False)
        self.checkBox2 = QtWidgets.QCheckBox("WeaveLabyrintti", self)
        self.checkBox2.move(300, 100)
        self.checkBox2.setVisible(False)
        self.checkBox2.clicked.connect(lambda: self.__changeSelection())
        self.checkBox1.clicked.connect(lambda: self.__changeSelection())

        ''' create button in the menu for generating the maze '''
        self.generoi = QtWidgets.QPushButton("Generoi", self)
        self.generoi.clicked.connect(lambda: self.buttonClicked())
        self.generoi.resize(100, 30)
        self.generoi.move(290, 200)
        self.generoi.setStyleSheet("border: 2px solid black")
        self.generoi.setVisible(False)

        ''' button for choosing the size '''
        self.leveysBox = QtWidgets.QSpinBox(self)
        self.leveysBox.move(300, 160)
        self.leveysBox.resize(70, 30)
        self.leveysBox.setMinimum(15)
        self.leveysBox.setMaximum(50)
        self.leveysBox.setVisible(False)

        ''' second title '''
        self.label2 = QtWidgets.QLabel("Anna leveys/korkeus", self)
        self.label2.setFont(font)
        self.label2.move(290, 130)
        self.label2.setVisible(False)

        ''' information about the maze size '''
        self.label3 = QtWidgets.QLabel(
            "Leveys/korkeus (min = 15, max = 50)", self)
        self.label3.move(380, 170)
        self.label3.setVisible(False)

    def showWindow(self):
        ''' Show window '''
        self.show()

    def __changeSelection(self):
        ''' Change maze settings '''
        sender = self.sender()
        if(sender.text() == "Tavallinen 2DLabyrintti"):
            self.checkBox1.setChecked(True)
            self.checkBox2.setChecked(False)
        else:
            self.checkBox1.setChecked(False)
            self.checkBox2.setChecked(True)

    def settingsMenu(self):
        ''' hide or show settings menu '''
        if not(self.checkBox1.isVisible()):
            self.checkBox1.setVisible(True)
            self.checkBox2.setVisible(True)
            self.label1.setVisible(True)
            self.label2.setVisible(True)
            self.label3.setVisible(True)
            self.leveysBox.setVisible(True)
            self.generoi.setVisible(True)
        else:
            self.checkBox1.setVisible(False)
            self.checkBox2.setVisible(False)
            self.label1.setVisible(False)
            self.label2.setVisible(False)
            self.label3.setVisible(False)
            self.leveysBox.setVisible(False)
            self.generoi.setVisible(False)

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        if(self.state == 0):
            painter.drawRect(274, 24, 501, 501)
            painter.fillRect(275, 25, 500, 500, QtGui.QColor("#E0E0E0"))
        if(self.state == 1):
            self.maze.drawMaze(self)
        if(self.state == 2):
            self.maze.drawMaze(self)
            self.player.drawPlayer(self)
        if(self.state == 3):
            self.maze.drawMaze(self)
            self.demo.drawRoute()
        painter.end()

    def buttonClicked(self):
        sender = self.sender()
        self.buttonListener.handleButtonClick(sender)

    def keyPressEvent(self, e):
        if(self.state == 2):
            self.keyListener.handleKeyPress(e)
