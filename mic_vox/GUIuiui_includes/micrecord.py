#Class of ringmemory:

import pyaudio
import wave
import datetime
import os
import threading




class micvox(threading.Thread):
    
    def __init__(self, pretime = 1, posttime = 3, looptime = 10, sens = 5):
        
        threading.Thread.__init__(self)
        

        #Initialize parameters:
        self.runstate = True
        
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1    
        self.RATE = 44100                            #Sampling rate 
        self.pretime = pretime                             #Recording time in seconds before trigger event
        self.posttime = posttime                            #Recording time in seconds after trigger event
        self.looptime = looptime                           #Recording loop time
        
        self.reftime = 1
        self.ref0 = 0
        self.avrg = 100
        self.ref = 10*self.avrg
        self.sens = sens
        
        self.ci = 0
        self.recording = False
        self.rec0 = 0
        self.rec1 = 0
        self.peak = False
        
        self.cycle     = [bytes(self.CHUNK*2) for i in range(0, 43*self.looptime)]    #Ringmemory with CHUNKS (a CHUNK has 1024 2-byte-values)
        self.cycleavrg = [1000           for i in range(0, 43*self.looptime)]    #Ingteger value of ringmemory   
        self.intchunk  = [0              for i in range(0, self.CHUNK)      ]    #One Chunk in integers
        
        self.reccycle = []                                               #For recording part of ringmemory
        
        
    def run(self):
        
        print("running...")

        self.p = pyaudio.PyAudio()                                                           #Create new stream object
        self.stream = self.p.open(format=self.FORMAT,
                        channels=self.CHANNELS, 
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        
        
        #*****************************************************************************
        #Loop:
        while(self.runstate):
            self.cycle[self.ci] = self.stream.read(self.CHUNK)
            
                
            #Extract peak value from bytes array (current stream-CHUNK):
            for ii in range(0, int(self.CHUNK)):
                self.intchunk[ii] = abs(int.from_bytes(self.cycle[self.ci][2*ii:2*ii+2], byteorder="little", signed=True))
            
            self.cycleavrg[self.ci] = int(sum(self.intchunk) / self.CHUNK)
            
             
            
            #Setting reference for peak detection:
            if (self.ci - 43*self.reftime) < 0:
                self.ref0 = self.ci + 43*(self.looptime - self.reftime)         #in case of an underflow
                
                self.avrg = int((sum(self.cycleavrg[self.ref0:43*self.looptime])+sum(self.cycleavrg[0:self.ci]))/43*self.reftime)
            
        
            else:
                self.avrg = int(sum(self.cycleavrg[self.ci-43*self.reftime:self.ci])/43*self.reftime)
            
            
            
            
            self.ref = 4*self.sens*self.avrg
            
            #Compare peak & ref:
            if max(self.intchunk) > self.ref:
                self.peak = True
            else:
                self.peak = False
            
            
            
            
            #Setting indexes and saving pre-record
            if self.peak == True and self.recording == False:  
                
                print("* start recording")
     
                self.recording = True
                if (self.ci - 43*self.pretime) < 0:
                    self.rec0 = self.ci + 43*(self.looptime - self.pretime)     #in case of an underflow
                    self.rec1 = self.ci + 43*self.posttime                 #In case of no overflow
                    
                    self.reccycle.extend(self.cycle[self.rec0:43*self.looptime])
                    self.reccycle.extend(self.cycle[0:self.ci])
                elif (self.ci + 43*self.posttime) > 43*self.looptime:
                    self.rec1 = self.ci + 43*(self.posttime - self.looptime)    #In case of an overflow
                    self.rec0 = self.ci - 43*self.pretime                  #In case of no underflow
    
                    self.reccycle.extend(self.cycle[self.rec0:self.ci])
                else:
                    self.rec1 = self.ci + 43*self.posttime                 #For record ending...Scheiß Fehler eyyy               
                    self.reccycle.extend(self.cycle[self.ci - 43*self.pretime:self.ci])
                
                    
                
            
             
            #Attach post-record to list:               
            if self.recording == True:
                self.reccycle.append(self.cycle[self.ci])
            
            #Save finish slice of ringmemory(pre-record to post-record):
            if self.recording == True and self.ci == self.rec1:
                self.recording = False
                
                print("* done recording")
                
                #*********************************************************************
                #Create Filename with timestamp:
                self.timestamp = datetime.datetime.now()
                self.timestamp_str = self.timestamp.strftime("20%y.%m.%d_%H;%M;%S")
                self.WAVE_OUTPUT_FILENAME = str(self.timestamp_str + "rec.wav")
                print("File saved as: ", self.WAVE_OUTPUT_FILENAME)
                
                #*********************************************************************
                #Check target directory:
                try:
                    os.makedirs("records")
                except FileExistsError:
                    pass
                
                #*********************************************************************
                #Create new .wav file:
                self.wf = wave.open(os.path.join(os.path.dirname(__file__), "records", self.WAVE_OUTPUT_FILENAME), 'wb')
                self.wf.setnchannels(self.CHANNELS)
                self.wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                self.wf.setframerate(self.RATE)
                self.wf.writeframes(b''.join(self.reccycle))
                self.wf.close()  
                del self.reccycle
                self.reccycle = []
            
            
            
    
            #Increment loop index:
            self.ci = self.ci + 1
            if self.ci>=(43*self.looptime):
                self.ci = 0
        
        #*****************************************************************************
        #End of ringmemory:

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print("end of recorder...")

        return
        
    
    def stop(self):
        self.runstate = False
        return
    
  
