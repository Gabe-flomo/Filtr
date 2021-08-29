"""

"""
import librosa
import numpy as np
import os
import pandas
import pickle
import json
import matplotlib.pyplot as plt 

class Loader:
    """ Responsible for loading audio files """

    def __init__(self, sample_rate: int, duration: float, mono: bool):
        self.sample_rate = sample_rate
        self.duration = duration
        self.mono = mono

    def load(self, path: str):
        # load the audio file [get only the signal and exclude the sample rate]
        signal = librosa.load(path = path, sr = self.sample_rate, duration = self.duration, mono = self.mono)[0]
        return signal


class Padder:
    """ Responsible for applying padding to an array """ 

    def __init__(self, mode: str = 'constant'):
        # 
        self.mode = mode

    def left_pad(self, array, num_missing_items):
        '''Left pads an array with the mode. 
           [1,2,3,4] -> [0,0,0,1,2,3,4] '''

        
        # left pads an array with the num_missing_items
        # tuple indicates (number of items to left pad, number of items to right pad)
        padded = np.pad(array, (num_missing_items, 0), mode = self.mode)
        return padded

    def right_pad(self, array, num_missing_items):
        '''Right pads an array with the mode. 
           [1,2,3,4] -> [1,2,3,4,0,0,0] '''

        # Right pads an array with the num_missing_items
        # tuple indicates (number of items to left pad, number of items to right pad)
        padded = np.pad(array, (0, num_missing_items), mode=self.mode)
        return padded


class LogSpectrogramExtractor:
    """Responsible for extracting log spectrograms (in decibles) from a time series signal"""

    def __init__(self, fram_size, hop_length):
        self.frame_size = fram_size
        self.hop_length = hop_length

    def extract(self, signal):
        # extraxt the short time fourier transform for
        # returns an array of shape -> (1 + frame_size / 2, number of frames) which would be 513 frequency bins so we 
        # will cutoff the last bin to keep 512
        stft = librosa.stft(signal, n_fft = self.frame_size, hop_length = self.hop_length)[:-1]
        spectrogram = np.abs(stft)
        log_spectrogram = librosa.amplitude_to_db(spectrogram)
        return log_spectrogram


class MinMaxNormalizer:
    """Responsible for applying mon max normalization"""

    def __init__(self, min_val = 0, max_val = 1):
        self.min = min_val
        self.max = max_val
    
    def normalize(self, array):
        '''
        Example:
            array = [50, 55, 60, 65]
            min = 0
            max = 10

            1) Create a new array by calculating the differnce between the lowest array value and the entire array 
                array - array.min() -> [(50 - 50), (55 - 50), (60 - 50), (65 - 50)] = [0, 5, 10, 15] 

            2) Calculate the range of values in the array by subtracting the max value from the min value.
                array.max() - array.min() -> [65 - 50] = 15

            3) We obtain the normalized array by dividing the array created in step 1 by the arrays range calculated in step 2.
                [0, 5, 10, 15] / 15 = [0, .33, .67, 1]

            4) Calculate the differnce between specified maximum value and minimum value. 
               This value is the new maximum value in our normalized array.
                10 - 0 = 10
            
            5) Scale the normalized array by the new max value, which was calculated in step 4.
                [0, .33, .67, 1] * 10 = [0, 3.3, 6.7, 10]
            
            6) add the min value.
                [0, 3.3, 6.7, 10] + 0 = [0, 3.3, 6.7, 10]
        '''

        # convert the array into a numpy array if it's passed as a list
        array = np.array(array) if isinstance(array, list) == True else array
        norm = (array - array.min()) / (array.max() - array.min()) 
        norm = norm * (self.max - self.min) + self.min
        return norm

    def denormalize(self, normalized_array, original_min, original_max):
        """ Inverts the normalization process 
        
            Example
            -------------------------
            array = [0, 3.3, 6.7, 10]
            original_min = 50
            original_max = 65

            1) Calculate the difference between the normalized array and the specified minimum
                (normalized_array - self.min) -> [0, 3.3, 6.7, 10] - 0 = [0, 3.3, 6.7, 10]
            
            2) Divide the array calculated in step 2 by the difference between the specified min and max values.
                min - max -> 10 - 0 = 10
                [0, 3.3, 6.7, 10] / 10 = [0, .33, .67, 1]

            3) Calculate the range of the original max and min values
                original_max - original_min -> 65 - 50 = 15

            4) Find the product of the range calculated in step 3 and the array from step 2
                [0, .33, .67, 1] * 15 = [0, 5, 10, 15]
            
            5) Add the original minimum value.
                [0, 5, 10, 15] + 50 = [50, 55, 60, 65]
            
            
            """
        # convert the array into a numpy array if it's passed as a list
        normalized_array = np.array(normalized_array) if isinstance(
            normalized_array, list) == True else normalized_array

        # rescales an array back into values between 0 and 1
        array = (normalized_array - self.min) / (self.max - self.min)

        # transforms it back to the original non-normalized array
        array = array * (original_max - original_min) + original_min
        return array 
 

class Saver:
    """Responsible to save features and the min max values """

    def __init__(self, features_path, min_max_path):
        self.features_path = features_path
        self.min_max_path = min_max_path

    def save_features(self, features, file_path):
        save_path = self._generate_save_path(file_path)
        np.save(save_path, features)

    def save_min_max_values(self, min_max_values):
        save_path = os.path.join(self.min_max_path, "min_max.pkl" )
        self._save(min_max_values, save_path)
    
    # @staticmethod
    def _save(self, data, save_path):
        with open(save_path, 'wb') as f:
            pickle.dump(data, f)

    def _generate_save_path(self, file_path):
        filename = os.path.split(file_path)[1][:-4]
        save_path = os.path.join(self.features_path, filename + ".npy")
        return save_path


class Vectorizer:
    """Preprocessing pipeline preprocesses audio in a directory, 
       applying the following steps: 
       
        Pseudocode
       ----------------------------------------------------------------
       1) load a file 
       2) pad the signal if necessary
       3) extract features
       4) normalize spectrogram
       5) save normalize spectrogram

       storing and saving the min max values for all the log spectrograms.
       """
    


    def __init__(self, objects: [dict, None] ):
        # create instances of the objects needed for the pipeline.
        self._loader = objects.get("loader", None)
        self.padder = objects.get("padder", None)
        self.extractor = objects.get("extractor", None)
        self.normalizer = objects.get("scaler", None)
        self.saver = objects.get("saver", None)
        self.min_max_values = {}
        self._features = []

        # 44100 * 10 = 441000 expected samples
        self._expected_num_samples = int(self.loader.sample_rate * self.loader.duration)

    @property
    def loader(self):
        return self._loader

    @property
    def features(self):
        return np.array(self._features)
    
    @property
    def min(self):
        minimum = list(self.min_max_values.keys())[0]
        return self.min_max_values[minimum]['min']
    
    @property
    def max(self):
        maximum = list(self.min_max_values.keys())[0]
        return self.min_max_values[maximum]['max']
    
    @loader.setter
    def loader(self, loader):
        self._loader = loader
        self._expected_num_samples = int(loader.sample_rate * loader.duration)


    def fit(self, data_path, save = True):
        ''' 
        data_path
            - the path to the dataset you want to load 

        # point to a dataset in the filesystem 
        # walk through the  directories and subdirectories
        # locate all the files 
        # load each file  
        # check to see if the file needs padding
        # if it does need padding, check to see how much padding it needs
        # apply the amount of neseccary padding to the signal and return it
        # use the feature extractor on the padded signal
        # normalize the extracted features
        # save the feature vector as a file        '''

        # loop through ever directory and subdirectory in the path
        print(f"Extracting features from {data_path}")
        for (root, subdirs, files) in os.walk(data_path):
            # loop through every file 
            for f in files:
                file_path = os.path.join(root, f)
                # print(file_path)
                if not file_path.endswith(".wav"):
                    # print(file_path)
                    continue
                self._process_file(file_path)
                # print(f"Processed file: {file_path}")

            if save:
                self.saver.save_min_max_values(self.min_max_values)

    def _process_file(self, file_path, save = True):
        
        signal = self.loader.load(file_path)
        if self._needs_padding(signal):
            # pad the signal 
            signal = self._apply_padding(signal)

        # extract features 
        features = self.extractor.extract(signal)

        # normalize the features
        normalized = self.normalizer.normalize(features)
        self._features.append(normalized)
        save_path = 'min_max_values'
        # save the extracted features
        if save:
            save_path = self.saver.save_features(normalized, file_path)

        # store min max values
        self._store_min_max(save_path, features.min(), features.max())

    def _needs_padding(self, signal):
        ''' Resposible for calculating the expected number of samples for a given duration.
            This is how we get a fixed length vector 👏🏾 '''

        if len(signal) < self._expected_num_samples:
            return True 
        return False

    def _apply_padding(self, signal):
        # calculate number of missing samples (expected sample rate - signal sample rate)
        num_missing_samples = self._expected_num_samples - len(signal)
        padded_signal = self.padder.right_pad(signal, num_missing_samples)
        return padded_signal

    def _store_min_max(self, save_path, min_val, max_val):
        self.min_max_values[save_path] = {
            "min": min_val,
            "max": max_val
        }

if __name__ == '__main__':
    
    sr = 44100
    duration = 8
    mono = True
    frame_size = 512
    hop_length = 256
    sample_rate = 44100

    spectrograms_dir = r"..\Data\audio_vectors\features"
    min_max_dir = r"..\Data\audio_vectors\min_max_values"
    dataset = r"E:\Sample library\Mugg Essentials\loops"

    # instantiate objects 
    objects = {}
    objects["loader"] = Loader(sample_rate, duration, mono)
    objects["padder"] = Padder()
    objects["extractor"] = LogSpectrogramExtractor(frame_size, hop_length)
    objects["scaler"] = MinMaxNormalizer()
    objects["saver"] = Saver(spectrograms_dir, min_max_dir)

    vectorizer = Vectorizer(objects)

    vectorizer.fit(dataset, save = False)
    print(vectorizer.features.shape)
    print(vectorizer.min)
    print(vectorizer.max)
    feat = vectorizer.features
    for f in feat[:5]:
        # fig, ax = plt.subplots(2,2)
        plt.imshow(f)
        plt.show()


    path = r"E:\Sample library\2021\monte booker sounds\sounds tape\fm\FM Monte FX.wav"
    # array = [1,2,3,4,5]
    # scaler = MinMaxScaler()
    # print(array)
    # print(scaler.normalize(array))
    # print(scaler.denormalize(scaler.normalize(array), 1, 5))
    # print(len(Loader(sr, duration, mono).load(path)))
    # print(f"Before padding: {array} \nAfter Padding: {Padder().right_pad(array, 5)}")
    # print(LogSpectrogramExtractor(fram_size=FRAME_SIZE,
    #                               hop_length=HOP_LENGTH).extract(Loader(sr, 
    #                                                                     duration, 
    #                                                                     mono).load(path)))
