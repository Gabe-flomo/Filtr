import os
import random
import shutil
import time
import pandas as pd
import json
import wave
from DSP import DSP 
import pathlib

class Folder(DSP):
    def __init__(self, path, walk = False):
        start = time.perf_counter()
        # super.__init__()
        self.allowed = ['.wav', '.mp3']
        self.root_path = path
        data = self.scan(self.root_path, deep = walk)
        self.frame = self.create_dataframe(data)
        end = time.perf_counter()
        print(f"Initialized in {end - start} seconds")
        self.prev = None
        self.next = None

    def create_dataframe(self, data):
        ''' create a dataframe for the files/directories in the path '''
        return pd.DataFrame(data).sort_values(by = 'type')


    ############ properties #############
    @property
    def name(self):
        pass
    @property
    def files(self):
        pass
    @property
    def file_count(self):
        pass
    @property
    def has_children(self):
        pass
    @property
    def is_child(self):
        pass
    @property
    def children(self):
        pass

    ########## Collection methods ############

    def _immediate_directory(self,path):
        """returns data in the immediate folder as a list """

        dirs = []
        
        # scan the directory
        with os.scandir(path) as dir:
            # look at each file/folder in the root path
            for entry in dir:
                # dont include files that start with '.'
                if not entry.name.startswith((".", "__")):
                    # get the full path of the file/folder
                    full_path = entry.path
                    # get the type of the entry
                    entry_type = self.get_type(full_path)

                    # only accept files that are allowed by the class
                    if entry_type == 'file':
                        ext = self.get_file_extension(full_path)
                        if ext not in self.allowed:
                            # print(f"This is a {ext} file and will be skipped")
                            # skip the file and continue the loop
                            continue

                    # is this entry in the root directory
                    is_in_root = self.in_root(full_path)
                    # get the directory that this file/folder is a child of
                    parent = self.get_parent(full_path)
                    # see if the folder has children
                    children = self.has_children(full_path)
                    # get the file duration
                    length = self.duration(full_path)

                    # add data as a row    
                    row = {
                        'name': entry.name,
                        'path': full_path,
                        'type': entry_type,
                        'parent': parent,
                        'has_children': children,
                        'in_root': is_in_root,
                        'length': length
                    }

                    dirs.append(row)
            
        yield from dirs

    def _walk_directories(self, path):
        ''' returns the data in the immediate folder and all child solders as a list of dictionaries '''
        data = []
        foldercount = 0
        # start the walk
        for (root, subdirs, files) in os.walk(path):
            # print(f"Current root: {os.path.basename(root)}")
            foldercount += 1
            # scan the current root and return data from the scan
            dirs = self._immediate_directory(root)
            # extend the current data list
            data.extend(dirs)  

        print(f"searched {foldercount} directories")
        # return the data
        return data    

    def scan(self, path, deep = False):
        ''' returns the data in the immediate folder and/or all child solders as a list of dictionaries '''
        # do a shallow scan
        if deep == False:
            data = list(self._immediate_directory(path))
            return data
        # do a deep scan
        else:
            data = self._walk_directories(path)
            return data

    ##########    file methods    ############

    ##########    Check methods   ############
    

    def in_root(self, path):
        # get the path with the basename removed
        removed_basename = self.path_step(path) 
        # if the path with the basename removed is the same as the rooth path, return true
        if removed_basename == self.root_path:
            return True
        else: return False
    
    def path_step(self, path, cutoff=1):
        """Definition: a path step is movement throught a path that allows you to 
        move further backwards in a directory.
        path being the disired path to change and the cutoff being how far back in the directory 
        you would like to go.
        
        for example:

                path_step(C:\\Users\\gabe5\\Desktop\\Source\\ginseng drum kit VOL, 2)

                the new path would be 

                C:\\Users\\gabe5\\Desktop. """

        path = path.split("\\")
        path = path[:-cutoff]
        path = "\\".join(path)
        #print(path)
        return path

    def has_children(self, path):
        ''' checks if a directory has children '''
        # check if the path is a directory
        if os.path.isdir(path):
            # open the directory
            with os.scandir(path) as dir:
                # look at each file/folder in the path until it finds a new folder
                for entry in dir:  
                    if os.path.isdir(entry.path):
                        return True
                # return false if no directories were found
                return False
        else: return False

    ##########    get methods    #############


    def get_type(self, path):
        ''' checks to see if a path is a file or directory '''

        if os.path.isfile(path):
            return 'File'

        elif os.path.isdir(path):
            return 'Folder'

        else: return None

    def get_file_extension(self, path):
        ''' Returns the extension of a file '''

        if self.get_type(path) == 'file':
            ext = pathlib.Path(path).suffix
            return ext
        return None

    def get_parent(self, path):
        ''' lets you know which folder is a parent relative to the root path'''

        # first check if the folder/file path is the root path
        if path == self.root_path:
            return 'root'
        
        # first go up a single path step
        pathstep = self.path_step(path)

        # get the basename for this new path 
        base = os.path.basename(pathstep)

        # return the folder as the parent
        return base
    ########## operator overloading ##########

class Plot:
    pass

class DataRow:
    pass


class Labeler:
    """ Responsible for extracting a useful label from a filepath/name """

    def __init__(self):
        self.categories = {

            "Kick": [],
            "Snare": [],
            "Clap": [],
            "808": [],
            "Perc": [],
            "Hat": ["Open_hat", "Closed_hat", ],
            "Cymbal": [],
            "Ride": [],
            "Piano": [],
            "Electric_paino": [],
            "Guitar": [],
            "Woodwind": [],
            "Brass": [],
            "Synth": [],
            "Pad": [],
            "Foley": []



        }

    @property
    def labels(self):
        return list(self.categories.keys())

class Dataset(Labeler):
    
    def __init__(self, dataset):
        # initialize labeler
        super().__init__()

        # determine the type of the dataset that was passed   
        self.dataset = self._infer_dataset(dataset)
        self.dataset.drop('Unnamed: 0', axis = 1, inplace = True)
        
        # self.dataset = self.read_csv(dataset)
        
        # responsible for automatic labeling files
        # self.labeler = Labeler()

    
        


    def _infer_dataset(self, dataset):
        ''' Responsible for verifying the data that is being passed '''
        def is_list_of_dicts(lst):
            if all([isinstance(x, dict) for x in lst]):
                return True
            else:
                return False

        if isinstance(dataset, list) and is_list_of_dicts(dataset):
            dataset = pd.DataFrame(dataset)            
        elif isinstance(dataset, pd.core.frame.DataFrame):
            pass
        elif isinstance(dataset, str):
            dataset = pd.read_csv(dataset)
        else:
            raise TypeError('Dataset is an invalid type. Must be a path to a csv file, List of dictionaries, or Dataframe')
        
        return dataset

    def _infer_location(self, index):
        ''' Responsible for determining if the index passed was an acceptable option for an index location or
            checking if it was a slice.
        '''
        pass

    def _get_label(self, pattern):
        ''' Responsible for extracting a '''
        pass

    # def __getitem__(self, index):
    #     '''Responsible for returning the row of data at the specified index
    #        Returns a DataRow object
    #     '''
    #     pass

    # @property
    # def labels(self):
    #     ''' responsible for returning the labels of the dataset.
    #         returns a dictionary of labels and numeric value
    #     '''
    #     pass

         




class File:
    pass


# path = r"E:\Sample library\2021\Pierre Bourne Drum & Loop Kit"
# path = r"E:\Sample library\2021"
# path = r"E:\Sample library"
# folder = Folder(path, walk=False)
# print(folder.frame)
# folder.frame.to_csv("E:\Documents\My Projects\Filtr\Data\csv\d.csv")
# print(json.dumps(folder.scan(path, deep = True), indent = 4))
# folder.deep_scan(path)

# df = Dataset([{'hello':'world'}, {'Goodby':"world"}])
# print(df.labels)

path = r"E:\Documents\My Projects\Filtr\Data\csv\training_data.csv"
data = Dataset(path)
print(data.dataset.iloc[1][0])

for row in data.dataset.itertuples():
    print(row[1])







