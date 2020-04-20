
#Import all necessary packages:
import os
import threading
from win10toast import ToastNotifier

#*****************************************************************************
#Tosast popup for single messages:
class toast(threading.Thread, ToastNotifier):
    def __init__(self, title, msg, duration):
        
        threading.Thread.__init__(self)
        self.title = title
        self.msg = msg
        self.duration = duration
        return
        
    def run(self):
        self.iconpath = os.path.join(os.path.dirname(__file__), "icon.ico")
        self.show_toast(self.title, self.msg, self.iconpath, self.duration)

        '''Important therefore is to set the a property...
           >Einstellungen
           >System
           >Benachrichtigungen und Aktionen
           >Benachrichtigungen
           >Benachrichtingungen von Apps und anderen Absendern abrufen
        '''
        return(0)

