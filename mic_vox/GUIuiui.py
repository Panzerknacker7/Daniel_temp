#Graphical user interface for working with choughing and sneezing detection:

#Import all necessary packages:
import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QPlainTextEdit
from PyQt5.QtCore import pyqtSlot
import threading
from PyQt5.QtGui import QIcon
from win10toast import ToastNotifier
from pyqtgraph import PlotWidget, plot

#*****************************************************************************






    
#*****************************************************************************
#User interface:
class UI(QWidget):
    def __init__(self):
        super(UI, self).__init__()
        

        self.title = "Husten/Niesen Erkennung"
        self.description = "Dies ist eine\nhust-, und nies-Erkennung...\nViel Spaß damit!"
        self.heigth = 800
        self.width = 1000
        self.left = 0
        self.top = 30
        self.runstate = True  
        
  

        self.initUI()

        return

        
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.heigth)

        
        #Button1:
        self.button1 = QPushButton("Run!", self)
        self.button1.setToolTip("Come on, it´s not that difficult...")
        self.button1.move(750, 750)
        self.button1.setEnabled(True)        
        self.button1.clicked.connect(self.click_button1)

        #Button2:
        self.button2 = QPushButton("Cancel", self)
        self.button2.setToolTip("Quit program...")
        self.button2.move(850, 750)
        self.button2.clicked.connect(self.click_button2)
        
        #Description text:
        self.text = QPlainTextEdit(self)
        self.text.insertPlainText(self.description)
        self.text.move(690, 50)
        self.text.resize(300, 600)
    
    
    
        return(0)
    
    def buttonrun(self):
        self.button1.setText("Running...")
        self.button1.setEnabled(False)
        return(0)
    
    
    #*************************************************************************
    #Button action:
    @pyqtSlot()
    #Button1 click:
    def click_button1(self):
        self.buttonrun()
        return(0)
        
    #Button2 click:
    @pyqtSlot()
    def click_button2(self):
        self.runstate = False
        return(0)
    




#*****************************************************************************
class APP(threading.Thread, QApplication):
    def __init__(self):
        
        threading.Thread.__init__(self)
        self.runstate = True      
         
        
        
        return
        
      
       
    def run(self):
        self.app = QApplication(sys.argv) 
        self.window = UI()          

        self.window.show()
        
        self.app.exec_()




        
        

        self.runstate = False
        

        return(0)
    
    def leave(self):
        self.runstate = False
        return(0)
    



