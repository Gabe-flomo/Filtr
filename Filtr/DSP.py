''' File for audio processing '''
import wave
import traceback
import os


class DSP:

    def __init__(self):
        pass

    def duration(self,file):
        try:
            with wave.open(file, 'r') as audio:
                # gets the sample frequency or the samples per second
                frate = audio.getframerate()
                #print(f'frame rate: {frate}')
                # the number of frames
                nframes = audio.getnframes()
                #print(f'num of frames: {nframes}')
                # the duration in seconds
                duration = round(nframes/frate,2)
                
        except PermissionError as e:
            #print(f"The File: {os.path.basename(file)} could not be read.\nThe duration will be set to 0")
            # print(f"(Permission error) Cannot get the length of the folder '{os.path.basename(file)}'. Duration set to 0")            
            duration = 0
        except wave.Error as e:
            # print(f"(Wave error) file does not start with RIFF id '{os.path.basename(file)}'. Duration set to 0")
            duration = 0
        except Exception as e:
            # raise e
            # print(f"A {e} occurred at '{os.path.basename(file)}' The duration will be set to 0")
            duration = 0

        return duration
