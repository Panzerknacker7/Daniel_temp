import pyaudio
import wave
import datetime
import os



#Set parameters for saving microphone stream:
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1    
RATE = 44100                            #Sampling rate 
pretime = 1                             #Recording time in seconds before trigger event
posttime = 3                            #Recording time in seconds after trigger event
looptime = 10                           #Recording loop time

#Set ringmemory parameters:

ci = 0
avrg = 2000
recording = False
rec0 = 0
rec1 = 0
peak = False


p = pyaudio.PyAudio()                                                           #Create new stream object

stream = p.open(format=FORMAT,
                channels=CHANNELS, 
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)









default = stream.read(CHUNK)
cycle = [bytes(CHUNK*2) for i in range(0, 43*looptime)]
#for i in range(0, 43*looptime):
#    cycle.append(default)

reccycle = []
intcycle = [0 for i in range(0, int(CHUNK/2))]
#*****************************************************************************
#Loop:
try:
    while(True):
        cycle[ci] = stream.read(CHUNK)
        
        #Setting reference for peak detection:
        for ii in range(0, int(CHUNK/2)):
            intcycle[ii] = int.from_bytes(cycle[ci][2*ii:2*ii+2], byteorder="little", signed=True)
            
        
        if max(intcycle) > 200 and recording == False:
            peak = True
        elif recording == True:
            peak = True
        else:
            peak = False
        
        #Setting indexes and saving pre-record
        if peak == True and recording == False:
            print("* start recording")
            recording = True
            if (ci - 43*pretime) < 0:
                rec0 = ci + 43*(looptime - pretime)     #in case of an underflow
                rec1 = ci + 43*posttime                 #In case of no overflow
                
                reccycle.extend(cycle[rec0:43*looptime])
                reccycle.extend(cycle[0:ci])
            elif (ci + 43*posttime) > 43*looptime:
                rec1 = ci + 43*(posttime - looptime)    #In case of an overflow
                rec0 = ci - 43*pretime                  #In case of no underflow

                reccycle.extend(cycle[rec0:ci])
            else:
                rec1 = ci + 43*posttime                 #For record ending...Scheiß Fehler eyyy               
                reccycle.extend(cycle[ci - 43*pretime:ci])
            
                
            
        
         
        #Attach post-record to list:               
        if recording == True:
            reccycle.append(cycle[ci])
        
        #Save finish slice of ringmemory(pre-record to post-record):
        if recording == True and ci == rec1:
            recording = False
            print("* done recording")
            #*********************************************************************
            #Create Filename with timestamp:
            timestamp = datetime.datetime.now()
            timestamp_str = timestamp.strftime("20%y.%m.%d_%H;%M;%S")
            WAVE_OUTPUT_FILENAME = str(timestamp_str + "rec.wav")
            print("File saved as: ", WAVE_OUTPUT_FILENAME)
            
            #*********************************************************************
            #Check target directory:
            try:
                os.makedirs("records")
            except FileExistsError:
                pass
            
            #*********************************************************************
            #Create new .wav file:
            wf = wave.open(os.path.join(os.path.dirname(__file__), "records", WAVE_OUTPUT_FILENAME), 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(reccycle))
            wf.close()  
            del reccycle
            reccycle = []
        
        
        

        #Increment loop index:
        ci = ci + 1
        if ci>=(43*looptime):
            ci = 0

#*****************************************************************************
#End of ringmemory:
except KeyboardInterrupt:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("end")
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("end")















































#Hier unverändertes Speichern....






    
'''
   
#*********************************************************************
#Create Filename with timestamp:
timestamp = datetime.datetime.now()
timestamp_str = timestamp.strftime("20%y.%m.%d_%H;%M;%S")
WAVE_OUTPUT_FILENAME = str(timestamp_str + "rec.wav")
print("File saved as: ", WAVE_OUTPUT_FILENAME)

#*********************************************************************
#Check target directory:
try:
    os.makedirs("records")
except FileExistsError:
    pass

#*********************************************************************
#Create new .wav file:
wf = wave.open(os.path.join(os.path.dirname(__file__), "records", WAVE_OUTPUT_FILENAME), 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(reccycle))
wf.close()  
        


stream.stop_stream()
stream.close()
p.terminate()
print("end")

'''