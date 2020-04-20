# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 19:33:52 2020

@author: HP
"""
import sys, os, threading
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time



class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.title = "Husten/Niesen Erkennung"
        self.description = "Dies ist eine\nhust-, und nies-Erkennung...\nViel Spaß damit!"
        self.heigth = 800
        self.width = 1000
        self.left = 0
        self.top = 30
        self.icon = QIcon(os.path.join(os.path.dirname(__file__), "GUIuiui_includes", "icon.ico"))
        self.runstate = True  
        
        self.initMW()
        
        
    def initMW(self):
        
        #Menu:
        self.statusBar().showMessage("Husten und Niesen Erkennung Hauptfenster")
        
        Close = QAction("&Exit", self)
        Close.setShortcut("Ctrl+E")
        Close.setStatusTip("Close application...")
        Close.triggered.connect(self.close)
        
        menubar = self.menuBar()
        file = menubar.addMenu("File")
        file.addAction(Close)
        
        #Button1:
        button1 = QPushButton("Close", self)
        button1.setToolTip("Close application...")
        button1.move(890, 750)
        button1.setEnabled(True)
        button1.clicked.connect(self.button1_press)
        
        #Button2:
        button2 = QPushButton("Run", self)
        button2.setToolTip("Run application...")
        button2.move(790, 750)
        button2.setEnabled(True)
        button2.clicked.connect(self.button2_press)
        
   
        #Window:
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.heigth)
        self.setWindowIcon(self.icon)
        


        
        self.show()
        
        
    #*************************************************************************    
        
    def button1_press(self):
        print("Exit button pressed!")
        self.runstate = False
        self.close()
        
    def button2_press(self):
        self.sender().setEnabled(False)
        self.sender().setText("Running...")
        print("Run button pressed!")
        
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.runstate = False
            self.close()

   
class newThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        
    def run(self):
        app = QApplication([])
        wind = MW()
        
        app.exec_()
        print("Exiting thrad:", self.name, "with ID", self.threadID)
        
    



print("active threads:", threading.active_count())

a = newThread(threadID = 1, name="meinThread")
a.start()
i = 0
while(a.is_alive()):
    print("Fuck you!", i)
    time.sleep(0.05)
    i += 1

a.join()


print("finally active threads:", threading.active_count())