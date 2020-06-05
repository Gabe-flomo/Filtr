from filtr import Filtr
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import IPython.display
import librosa
import librosa.display
from scipy.io import wavfile
import sys
import wavio
import soundfile as sf

Data_path = "D:\\Documents\\Atom\\myrepos\\Filtr\\Filtr\\Audio"
Categories = ['Kick']
f = Filtr(Data_path,dest = "D:\\Documents\\Atom\\myrepos\\Filtr\\Filtr\\Images")
full_path = ''
training_data = []
training_names = []

for category in Categories:
    full_path = os.path.join(Data_path,category)
    files = f.files(full_path)
    os.chdir(full_path)
    print(category)
    for file in files:
        #print(file)
        training_names.append(file)
        
'''def audio_data(training_names,type = None):
    audio_info = []
    sr = 0
    for i in range(len(training_names[:5])):
        try:
            # loading the data
            #sr,data = wavfile.read(training_names[i])
            #rate, sampwidth, data = wavio.read(training_names[i])
            data, sr = librosa.load(training_names[i],mono = True,duration = 1.5,res_type = 'scipy')
            #data = data[:, 0]
            #print(data[:5])

            # harmonic percussive separation
            #harmonic, percussive = librosa.effects.hpss(data)
            
            if type is None:
                audio_info.append(data)
            elif ('P' or 'p' or 'perc') in type:
                audio_info.append(percussive)
            elif ('H' or 'h' or 'harm') in type :
                audio_info.append(harmonic)
        except:
            #print(e)
            print(f"there was an error loading this file: {training_names[i]}")
            print("Unexpected error:", sys.exc_info()[0])
            #print()
            raise
            pass
        
    return audio_info'''

def audio_data(training_names,type = None):
    audio_info = []
    sr = 0
    
    for name in training_names:
        try:
            # loading the data
            #sr,data = wavfile.read(name)
            data, samplerate = sf.read(name)
            #rate, sampwidth, data = wavio.read(name)
            #data, sr = librosa.load(name,mono = True,duration = 1.5,res_type = 'scipy')
            #data = data[:, 0]
            #print(data[:5])
            #print(data)
            # harmonic percussive separation
            #harmonic, percussive = librosa.effects.hpss(data)
            
            if type is None:
                audio_info.append(data)
            elif ('P' or 'p' or 'perc') in type:
                audio_info.append(percussive)
            elif ('H' or 'h' or 'harm') in type :
                audio_info.append(harmonic)
        except:
            #print(e)
            print(f"there was an error loading this file: {name}")
            print("Unexpected error:", sys.exc_info()[0])
            #print()
            raise
            
        
    return audio_info

data = audio_data(training_names) 
print(len(data))  