#This is a test to use methods of the class micvox to easyly work with the recorder.


from GUIuiui_includes.micrecord import micvox                     #Audiorecorder
from GUIuiui_includes.breakfest import toast
from GUIuiui_includes.gui import APP
import threading





    
try:

    print("start")
   
    #Audiorecorder:
    newrecorder = micvox()
    newrecorder.start()   
    
    #Toast notification:
    newpop = toast("Ufbasse:", "software has been started", 2)
    newpop.start()     

    #Interface:
    newapp = APP()
    newapp.start()    
 

    #*************************************************************************
    #Mainloop:
    print(threading.active_count(), " threads are active")
    print(threading.enumerate(), " are the active threads")
    
    
    while(True):
        pass

        
        
       
        
    #*************************************************************************
    #End of mainloop:
    newrecorder.stop()
    print("end mainloop")
    print(threading.active_count(), " threads are active")
    print(threading.enumerate(), " are the active threads")

    
except:  
    newrecorder.stop()
    newrecorder.join()
    newpop.join()
    newapp.leave()
    newapp.join()


    print("exception...")
    
    print(threading.active_count(), " threads are active")
    print(threading.enumerate(), " are the active threads")

