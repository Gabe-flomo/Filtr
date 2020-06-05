import os
import random 
import shutil
import time
import concurrent.futures as future
from multiprocessing import Process
import queue
import wave
import re
import librosa
import soundfile as sf
from scipy.io import wavfile
from .failures import errors
import wavio
import json



class Filtr():

    def __init__(self,path = None,dest = None):
        """ initializes the class with current path"""

        # sets the path passed into the constructor as the current working path
        if path is None:
            raise errors.NoPathError
        else:
            self.current_path = path
            os.chdir(self.current_path)

        # a list of paths that were recently visited
        self.previous_paths = []
        self.visited = []

        # what is the current working directory (should be same as current_path)
        self.working_directory = os.getcwd()


        self.current_folder = ""
        self.current_destination = dest
        self.current_files = self.files(self.current_path)
        self.current_folders = self.folders(self.current_path)
        self.seen_files = []
        self.seen_folders = []
        self.filecount = 0
        self.foldercount = 0
        self.size = 0
        self.pending = []

    def __newpath__(self,name):
        return os.path.join(self.current_path,name)

    def __update__(self):
        os.chdir(self.current_path)
        self.current_files = self.files(self.current_path)
        self.current_folders = self.folders(self.current_path)
        self.working_directory = os.getcwd()

    def __workingdir__(self,path):
        self.current_path = os.chdir(path)

    def _get_key(self,val,dic):
        for key, value in dic.items():
            if val == value['filename']:
                return key

    def _deletefile(self, file):
        os.remove(file)

    def _pad(self, records, file):
        ''' used to add equal space between text '''
        filenames = []
        if type(records) == dict:
            for key in records.keys():
                filenames.append(records[key]['filename'])
            
        width = max(len(f) for f in filenames) + 5
        padding = width - len(file)
        space = " " * padding
        return space

    def _save_records(self,path, ignore = None, sortby = 'length'):
        ''' saves a records dictionary as a json file for faster file searching '''

        records = self.filetree(path=path, ignore=ignore, sortby=sortby)
        #

        with open(r'E:\Documents\My Projects\Filtr\Data\JSON\records.json', 'a') as outfile:
            json.dump(records, outfile)

        print(r'Records saved to E: \Documents\My Projects\Filtr\Data\JSON\records.json')

    def _load_records(self):
        ''' loads the records that were saved '''
        with open(r'E:\Documents\My Projects\Filtr\Data\JSON\records.json', 'r') as infile:
            self.records = json.loads(infile.read())

        return self.records

    def info(self,path = None,detail = False):
        """This function checks to see if a directory has sub-directoies all the way
        down to the last directory with subdrectories in it"""

        ## creates a list with all the entries in the path
        dirs = self.folders(path) if path is not None else self.folders()
        files = self.files(path) if path is not None else self.files()

        # adds all the files and directories that it's encountered into a list
        self.seen_files.append(str(files) + " ")
        self.seen_folders.append(str(dirs) + " ")
        self.foldercount += len(dirs)
        self.visited.append(path)
        
        if len(dirs) == 0:
            SF = self.files()
            self.filecount += len(SF)
        
        for count,dir in enumerate(dirs):
            # creates a temporary path from the passed path and the folder that its on
            tempath = os.path.join(path,dir)
            
            # counts how many subdirectories are in that path
            SD = self.folders(tempath)
            
            # if there are no sub directories, check to see if there are any files
            if len(SD) == 0:
                SF = self.files(tempath)
                self.filecount += len(SF)
                self.seen_files.append(str(SF) + " ")
                if detail:
                    print(f"There were no more directories in the folder {dir}\nand there were {len(SF)} files")
                    print()
                
            else:
                if detail:
                    print(f"#{count+1} {dir} contains these child directories \n {SD}")

                return self.info(tempath)


        x = self.visited.pop(0)
        for path, dirs, files in os.walk(x):
            for f in files:
                fp = os.path.join(path, f)
                self.size += os.path.getsize(fp)
            


                
        # a sample of all of the seen folders
        sample = self.seen_folders[0]
    
        print(f"There were {self.foldercount} folders total including:")
        print(f"{sample}\n")
        print(f"There were {self.filecount} files total\n")
        print(f"Size of {os.path.basename(x)}: {round(self.size/1000000,2)}MB")
   
    def folders(self,path = None):
        """This function lists only the directories in a path and 
        exludes the files and returns a list of the directories"""

        dirs = []
        if path is not None:
            with os.scandir(path) as dir:
                for folder in dir:
                    if not folder.name.startswith(".") and folder.is_dir():
                        dirs.append(folder.name)
            self.current_folders = dirs
            return dirs
        else:
            with os.scandir() as dir:
                for folder in dir:
                    if not folder.name.startswith(".") and folder.is_dir():
                        dirs.append(folder.name)
            self.current_folders = dirs
            return dirs

    def files(self,path = None, ignore = None):
        """This function lists only the files in a path and 
        exludes the directories and returns a list of the files"""

        # create an empyt dict to store filenames and data
        dirs = {}
        ignore = tuple(ignore) if ignore is not None else ""
        if path is not None:
            with os.scandir(path) as files:
                for count, file in enumerate(files):
                    if file.name.endswith(ignore):
                        # print(file.name)
                        continue
                    else:
                        if (not file.name.startswith(".") and file.is_file()):
                            dirs[count] = {}
                            dirs[count]['filename'] = file.name
                            dirs[count]['path'] = os.path.join(path, file.name)
                            dirs[count]['type'] = file.name[-4:]
                            dirs[count]['duration'] = self.duration(os.path.join(path, file.name))
            self.current_files = dirs
            return dirs
        else:
            with os.scandir() as files:
                for count, file in enumerate(files):
                    if file.name.endswith(ignore):
                        # print(file.name)
                        continue
                    else:
                        if (not file.name.startswith(".") and file.is_file()):
                            dirs[count] = {}
                            dirs[count]['filename'] = file.name
                            dirs[count]['path'] = os.path.join(self.current_path, file.name)
                            dirs[count]['type'] = file.name[-4:]
                            dirs[count]['duration'] = self.duration(os.path.join(self.current_path, file.name))
            self.current_files = dirs
            return dirs

    def filetree(self, path=None, ignore=None, sortby = None, reject = False):
        """
        Used to scan all of the files in a root directiory. Instead of only checking the immediate folder
        it checks all subfolders as well and returns a dictionary of file information.

        parameters
        ---------------

        path: string
                A full path to a directory, if one is not provided it will use the the path that the class was last 
                pointing by self.current_path

        ignore: tuple
                Used to indicate which filetypes to ignore while searching the directory tree.
                ex.     ('.mp3','.ogg','.asd')

        sortby: string
                Used to sort how the files are stored based on a specified dictionary key.
                ex. sortby = Duration  

        """
        # check if the path is none or not and if it is, use the class path
        path = path if path is not None else self.current_path
        sortby = sortby.lower() if sortby is not None else sortby
        # print(path)
        records = {}
        index = 0

        # check which files to ignore
        ignore = tuple(ignore) if ignore is not None else ignore

        # start walking the directories
        for  (root, subdirs, files) in os.walk(path):

        # look for only the files
            for file in files:
                # check to makes sure the file type shouldnt be ignored
                
                if file.endswith(ignore):
                    
                    #print(f"{file} will not be added to dict")
                    if reject:
                        fullpath = os.path.join(root,file)
                        self._deletefile(fullpath)
                else:
                  # if not add to the file dict
                    records[index] = {}
                    records[index]['filename'] = file
                    records[index]['path'] = os.path.join(root, file)
                    records[index]['type'] = file[-4:]
                    records[index]['duration'] = self.duration(os.path.join(root, file))
                    index += 1

        # after all of the files have been generated, Check to see how to sort them
            # if sortby is provided, sort by that key
        if sortby == 'duration' or sortby == 'length':
            self.records = dict(sorted(records.items(), key=lambda record: record[1]['duration']))
        elif sortby == 'filename' or sortby == 'name':
            self.records = dict(sorted(records.items(), key=lambda record: record[1]['filename']))
        

        
        return self.records

    def viewrecords(self, records=None):
        ''' outputs the files from the filetree search '''
        records = self.records if records is None else records
        if records is None:
            raise TypeError('Records can not be of type None')

        keys = records.keys()
        for index, record in records.items():
            # adds 0s to the index to make them all the same length
            # for example:
            #    001)
            #    002)
            #    003)
            #    ...
            #    100)
            index = str(index+1).zfill(len(str(max(keys))))
            print(
                f"{index}) {record['filename']} {self._pad(records,record['filename'])} {record['duration']}")
        
        print(f'\nShowing {len(self.records)} records')
        
    def output(self,text,files = None, path = None,ext = False,ignore = None, reject = True):
        '''
        Takes in a string ('text') as an explicit command to display
        some output.

        -------------------------------------------------------------------------------
        output("folders") - will list the folders in the current working directory
        -------------------------------------------------------------------------------
        output("files") - will list all the files in the current working directory
        -------------------------------------------------------------------------------
        output("both") - will list both the files and folders in the working directory
        -------------------------------------------------------------------------------

        If ext is set to true the file extension will be visible.
        When displaying both, the file extension will always be visible.

        The ignore parameter expects a file type or types to ignore. It can be passed in
        either as a list or as a string. If nothing is passed in it will display all file types

        Reject  determines whether or not the ignored file should be deleted or not. By default
        this is True, meaning that any ignored file will also be deleted. If set to False, the ignored
        file will remain but wont be displayed.   

        '''
        
        text = text.lower()
        #duration = self.durations() if path is None else self.durations(path = path)

        # Filter files and output
        if text == ("files" or "file"):
            ignore = tuple(ignore) if ignore is not None else ignore
            file_list = self.files(ignore=ignore) if path is None else self.files(path,ignore)
            

            filtered = []
            if len(file_list) == 0:
                print("There are no files in this location")
            else:   
            # loop through files and check for conditions
                for index in file_list:

                    # condition 1         #
                    # dont show extension #
                    # show all files      #
                    # dont remove         #               
                    if (ext == False) and (ignore == None) and (reject == False):
                        file = os.path.splitext(file_list[file_list[index]]['filename'])
                        filtered.append(file[0])

                    # condition 2                                   #
                    # dont show extension                           #    
                    # show all files except for the ignored ones    #
                    # dont remove                                   #
                    elif (ext == False) and (ignore is not None) and (reject == False):
                        file = ["",""] if file_list[index]['filename'].endswith(ignore) else os.path.splitext(file_list[index]['filename'])
                        filtered.append(file[0])


                    # condition 3
                    # dont show extension
                    # show all files except for the ignored ones
                    # remove ignored files
                    elif (ext == False) and (ignore != None) and (reject == True):
                        
                        if file_list[index]['filename'].endswith(ignore):
                            os.remove(file_list[index]['filename'])
                        
                        else:
                            file = ["",""] if file_list[index]['filename'].endswith(ignore) else os.path.splitext(file_list[index]['filename'])
                            filtered.append(file[0])


                    # condition 4
                    # show extension
                    # show all files except for the ignored ones
                    # dont remove
                    elif (ext == True) and (ignore != None) and (reject == False):
                        file = "" if file_list[index]['filename'].endswith(ignore) else file_list[index]['filename']
                        filtered.append(file)
                    

                    # condition 5
                    # show extension
                    # show all files except for the ignored ones
                    # remove ignored files
                    elif (ext == True) and (ignore != None) and (reject == True):
                        if file_list[index]['filename'].endswith(ignore):
                            os.remove(file_list[index]['filename'])
                            file = ""
                            filtered.append(file)
                        
                        else:
                            filtered.append(file_list[index]['filename'])


                    # condition 6
                    # show extension
                    # show all files 
                    # keep all
                    elif (ext == True) and (ignore == None) and (reject == False):
                        filtered.append(file_list[index]['filename'])    

            width = max(len(f) for f in filtered) + 4

            # output files
            print("Name\t\t\t\tDuration")
            print("----\t\t\t\t--------\n")
            for count,file in enumerate(filtered):
                padding = width - len(file)
                space = " " * padding
                key = self._get_key(file_list[count]['filename'], file_list)
                count = str(count+1).zfill(2)
                if (file_list[key]['duration'] <= 60):
                    print(f"{count}) {file} {space} {round(file_list[key]['duration'],2)}")
                elif file_list[key]['duration'] > 60:
                    mins = file_list[key]['duration'] // 60
                    secs = file_list[key]['duration'] % 60
                    print(f"{count}) {file} {space} {mins}:{secs}")
                             

        # print the folders
        elif text == ("folders" or "folder"):
            folders = self.folders() if path is None else self.folders(path)
            if len(folders) == 0:
                print(f"there are {len(folders)} folders")
            else:    
                for count, folder in enumerate(folders):
                    print(f"{count+1}) {folder}")           


        # print files and folders
        elif text == "both":
            files = self.files() if path is None else self.files(path)
            folders = self.folders() if path is None else self.folders(path)
            x = 0
            print()
            print(f"showing {len(folders)} folders")
            #print folders first
            for count, folder in enumerate(folders):
                print(f"{count+1}) {folder}")
                x = count + 1


            print()
            print(f"showing {len(files)} files")
            # print files next
            for key in files.keys():
                print(f"{key + 1}) {files[key]['filename']}")
         
        
        print()
           
    def formated(self, lists, case = ""):
        case = case.lower()
        if case == 'filepath':
            for index, file in enumerate(lists):
                print(f'{index+1}) {os.path.basename(file)}')
        else:
            for index, file in enumerate(lists):
                print(f'{index+1}) {file}')
    
    def xfer(self,file,dest = None):
        # t1 = time.perf_counter()
        if dest is None:
            dest = self.current_destination
            if type(file) == list:
                for i in file:
                    try:
                        shutil.copy(i, dest)
                    except:
                        continue
            else:
                try:
                    shutil.copy(file,dest)
                except:
                    pass
        else:
            if type(file) == list:
                
                for i in file:
                    try:
                        shutil.copy(i, dest)
                    except:
                        continue
            else:
                try:
                    shutil.copy(file, dest)
                except:
                    pass

        # t2 = time.perf_counter()
        # finish = t2-t1
        # print(f'finished in {round(finish,2)} seconds')
        return self

    def process(self, data = None,workers = os.cpu_count(), dest = None):
        """Counts how many logical processors there are on the machine and uses that number
        to determine how many queues to create. Each queue will get a portion of the total number 
        of files in the current directory or the directory that is being pointed to
        (files_per_queue = total_files / number_of_processors). 

        Each queue is then assigned to a process and the files in that queue will be moved within
        that process.

        ---------------------------------------
        Parameters 
        ---------------------------------------

         workers:

         determines the number processors to use, if nothing is given it will default to the maximum
         number.

         """
        # t1 = time.perf_counter()
        num_cpu = workers
        processes = []
        q = self.get_queues(workers) if data is None else self.get_queues(data = data, workers = workers)
        dest = self.current_destination if dest is None else dest
                
        for i in range(num_cpu):
            #print(i)
            target = q[i].get()
            p = Process(target = self.xfer, args=[target,dest])
            processes.append(p)

        for p in processes:
            p.start()

        for p in processes:
            p.join()


        # t2 = time.perf_counter()
        # finish = t2-t1

        #print(f'finished in {round(finish,2)} seconds')

    def get_queues(self,data = None,workers = os.cpu_count()):

        q = queue.Queue()
        num_cpu = workers
        print(f"CPUS: {num_cpu}")

        files = self.current_files if data is None else data
        if type(files) != list:
            raise TypeError(f"Files can not be type {files}")

        num_files = len(files)
        print(f"FILES: {num_files}")

        
        if num_files <= num_cpu * 2:
            quo = len(files)
            rmd = 0
        else:
            quo = num_files // num_cpu
            rmd = num_files % num_cpu

        print(f"quotient: {quo}")
        print(f"remainder: {rmd}")

        queues = []
        files_left = num_files
        #print(f"files left: {files_left}")
        filelist = []

        print("Generating Queues")
        while True:
            if len(files) == 0:
                break
            elif files_left == rmd:
                #print(f"files left: {files_left}")
                # for _ in range(rmd):
                #     #print(f"len: {len(files)}, position: {i}")
                #     file = files.pop()
                #     filelist.append(file)

                #print(f"filelist: {filelist}")
                q.put(files)
                queues.append(q)
                files_left -= rmd
            else:
                for _ in range(quo):
                    try:
                        file = files.pop()
                        filelist.append(file)
                    except:
                        pass

                q.put(filelist)
                
                queues.append(q)
                files_left -= quo
                
            #print(f"files left: {files_left}")
        
        
        return queues

    def access(self,index):
        """
        You can either enter an index location as an int or a string and the folder will be 
        opened and the class will be updated to work within the opened folder
        """
        folders = self.folders()
        name = folders[index-1] if type(index) == int else index
        print(f"Opening: {name}")
        self.previous_paths.append(self.current_path)
        self.current_path = self.__newpath__(name)
        self.__update__()
        return self

    def back(self):
        """
        Will bring the working directory up a level to the parent directory.

        """
        print(f"\nPrevious paths: {self.previous_paths}")
        self.current_path = self.previous_paths.pop()
        self.__update__()
        print(f"going back to: {os.path.basename(self.current_path)} \n")
        return self
        
    def path_step(self,path,cutoff = 1):
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

    def class_info(self):
        print(f"The current path is {self.current_path}")
        print(f"The current working directory is {self.working_directory}")
        print(f"The current destination is {self.current_destination}\n")
        print(f"The current folders are {self.current_folders}\n")
        print(f"The current files are {self.current_files}\n")
        print(f"Previously visited paths are {self.previous_paths}\n")

# move to DSP      
    def durations(self,path = None):
        """
        function that will return the duration of a file
        """

        files = self.files(path) if path is not None else self.files()
        durations = []
        for file in files:
            try:
                # load the audio data 
                data, sr  = librosa.core.load(file)
                duration = librosa.core.get_duration(data, sr=sr)
                durations.append(duration)
            except:
                print(f"The File: {file} is an unsupported type and \nits duration could not be calculated.\n")
                duration = 0
                durations.append(duration)

        return durations

# move to DSP
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
                
        except :
            #print(f"The File: {os.path.basename(file)} could not be read.\nThe duration will be set to 0")
            duration = 0

        return duration

    def generate(self, keyword, paths=None, saved_records = True, datalimit=25, dest=None, ban= None, duration_limit=15, kw_in_dir = True, verify = True, degree = 3 ,ignore = None, multiprocess = True, verbose = False):
        ''' Takes in a keyword and searches the paths for the keyword in filenames.

        parameters
        ----------
        keyword -> string:
            specifies what types of filenames to look for. 

                For example:
                keyword = kick, will only look for files with "kick" in the names

        path -> tuple:
            Specifies the paths to walk through

        limit -> int:
            Specifies when to stop looking for files

        dest -> string:
            where to move the files

        ban -> list:
            Identifies which types of files to ignore and what folders not to look in.
            
                For example:
                ban = (loop,) -> will ignore directories with the word loop in it and files with the word loop in it

        duration_limit -> float:
            maximum length for a file

        kw_in_dir -> bool:
            If true, will search only the directories with the keyword in the name

        degree -> int:
            indicates how many directories from the file should be considered to determine
            whether or not 

        verbose -> bool:
            will print the output as it is generated

        verify -> bool:
            if kw_in_dir is true, verify is used to determine whether or not to still look for the keyword in the filename
        '''

        # make the path point somewhere, if None use the class path
        paths = paths if paths is not None else list(self.current_path)
        
        # make the dest point somewhere, if None use the class dest
        dest = dest if dest is not None else self.current_destination

        duration_limit = 100000 if duration_limit is None else duration_limit

        if datalimit < 25:
            raise errors.DataLimitError()

        # set up the ban
        bantype = type(ban)
        # print(f"ban type: {bantype}")
        if bantype == list:
            # print(f"Will not look in folders or files that contain {ban}")
            pass
        elif ban is None:
            ban = ""
        else:
            raise TypeError(f'Ban needs to passed as a list not as {type(ban)}')
        
        # handle ignores
        ignore =  tuple(ignore) if ignore is not None else ignore
        if ignore is None:
            raise TypeError(f'Ignore can not be of type {ignore}')

        
        # list of pending files to move
        pending = []
        counter = 0

        print('Generator Started')
        # loop throught the paths tuple
        if saved_records:
            # uses the records most recently saved from the _save_records method
            records = self._load_records()
            for index, data in records.items():
                counter += 1
                # check to make sure that the data limit has not been reached
                if len(pending) == datalimit:
                    break
                elif len(pending) < datalimit:
                    # get the file properties for each sample
                    properties = records[index]
                    # check to see if the file should be banned
                    # these are the files that will be allowed
                    if not self.contains(ban, properties['path']):
                        # check to see if the keyword is present in the path
                        if kw_in_dir:
                            if self.path_contains(keyword, properties['path'], degree=degree):
                                # if the keyword also has to be in the filename
                                if verify and self.contains(keyword, properties['filename']):
                                        #check if the duration is less than the duration limit
                                    if properties['duration'] <= duration_limit:
                                        #print(f"Adding {properties['filename']}")
                                        pending.append(properties['path'])
                                elif not verify:
                                    if properties['duration'] <= duration_limit:
                                        #print(f"Adding {properties['filename']}")
                                        pending.append(properties['path'])

                        # check to see if the keyword is in the filename
                        else:
                            if self.contains(keyword, properties['filename']):
                                # check if the duration is less than the duration limit
                                if properties['duration'] <= duration_limit:
                                    #print(f"Adding {properties['filename']}")
                                    pending.append(properties['path'])
                if len(pending) == datalimit:
                    print('data limit reached')
                    break
        else:
            # setup the path
            if paths is None:
                raise errors.NoPathError('A path need to be provided.')
            elif dest is None:
                raise errors.NoPathError('A destination need to be provided.')
            elif paths and dest is None:
                raise errors.NoPathError(
                    'A path and destination need to be provided.')

            for path in paths:
                # get the file records for each path
                records = self.filetree(path=path, ignore=ignore, sortby='length')
                # self.viewrecords()
                for index, properties in records.items():
                    counter += 1
                    # check to make sure that the data limit has not been reached
                    if len(pending) == datalimit:
                        break
                    elif len(pending) < datalimit:
                        # get the file properties for each sample
                        properties = records[index]
                        # check to see if the file should be banned 
                        # these are the files that will be allowed
                        if not self.contains(ban, properties['path']):
                            # check to see if the keyword is present in the path
                            if kw_in_dir:
                                if self.path_contains(keyword, properties['path'], degree=degree):
                                    if verify and self.contains(keyword, properties['filename']):
                                        # check if the duration is less than the duration limit
                                        if properties['duration'] <= duration_limit:
                                            #print(f"Adding {properties['filename']}")
                                            pending.append(properties['path'])
                                    elif not verify:
                                        
                                        if properties['duration'] <= duration_limit:
                                            #print(f"Adding {properties['filename']}")
                                            pending.append(properties['path'])

                            # check to see if the keyword is in the filename
                            else:
                                if self.contains(keyword, properties['filename']):
                                    # check if the duration is less than the duration limit
                                    if properties['duration'] <= duration_limit:
                                        #print(f"Adding {properties['filename']}")
                                        pending.append(properties['path'])
                if len(pending) == datalimit:
                    print('data limit reached')
                    break
                            

        print(f"Located {len(pending)} {keyword} files")
        if verbose:
            print('Verbose is set to True')
            print(f'Using the keyword: {keyword}')
            if not saved_records:
                print(f'Paths searched:')
                self.formated(paths)
            else:
                print(f'Used records. Length: {len(records)}')

            print(f'Banned folder types: {ban}')
            print(f'File Destination: {dest}')
            print(f'Use Multiprocessing: {multiprocess}')
            print(f'Data limit: {datalimit}')
            print(f"Searched through a total of {counter + 1} files")
            print(f'File duration limit: {duration_limit}')
            print(f'Only consider files with the keyword in the directory: {kw_in_dir}')

            if kw_in_dir:
                print(f'Using degree of: {degree}')
                
            print(f'Ignoring files of type: {ignore}')
            if len(pending) < 100:
                print()
                self.formated(pending,case = 'filepath')
            else:
                print('The file list is too large to display')

        if len(pending) > 0:       
            try:    
                if multiprocess:
                    self.process(data=pending, dest=dest)
                else:
                    self.xfer(pending, dest=dest)
            except Exception as e:
                print(f"There was an error:")
                self.xfer(pending, dest=dest)
                raise e
                
        else:
            print(f"There were no {keyword} files found.\nTry using a different keyword or checking to see if the keyword has been banned")

    def change_dest(self,newdest):
        self.current_destination = newdest
        print(f"New destination {self.current_destination}\n")

    def rename(self,keyword,newname,category_code = None,path = None,multiple = True,ext = '.wav'):
        '''
        renames a file based on the keyword to a new name.

        Parameters
        ----------
        keyword: (string or list)
        Specifies a key word to look for in the name of a file. All of the files with the keyword in the name can then be renamed
        to the new name.

        newname:
        Determines what the old file will be renamed to

        category_code: (string)
        When renaming multiple files you can use a category code to make sure that each of the renamed files 
        that is in the same category gets the same code.

        path: (string)
        The location of the files that you want to rename. by default this will be the current destination
        but can be manually entered.

        multiple: (bool or int)
        This paramater determines how many files will be selected to rename. By default this is set to true
        meaning that all the files that match the keyword will be renamed. Instead of setting to false, input 
        an integer to determine how many files to rename.
        '''

        self.previous_paths.append(self.current_path)
        path = path if path is not None else self.current_destination
        category_code = "" if category_code is None else category_code
        self.__workingdir__(path)
        files = self.files(path=path)
        try:
            ## if multiple is an integer run the loop as that many times
            if type(multiple) == int:
                for i in range(multiple):
                    # finding a file to work with
                    filename = files[i]
                    try:
                        # if keyword was passed as a list 
                        # check if any keyword is in the filename
                        if type(keyword) == list:
                            for word in keyword:
                                word = word.lower()
                                name = filename.lower()
                                try:
                                    # rename the file if the keyword is in the filename
                                    if word in name:
                                        os.rename(filename,newname + category_code + f'{i}' + ext)
                                except:
                                    print(f'File under the name {newname+i+ext} already exist line 648')

                        elif type(keyword) == str:
                            # if keyword is a string just check if the keyword is in the filename
                            keyword = keyword.lower()
                            name = filename.lower()
                            try:
                                if keyword in name:
                                    os.rename(filename,newname + category_code + f'{i}' + ext)
                            except:
                                print(f'File under the {newname+i+ext} already exist line 620') 
                    except:
                        print('Invalid type. Keyword must be of type int or list line 622')
            # if multiple is a boolean then look through all the files
            elif multiple:
                for i,file in enumerate(files):
                    try:
                        if type(keyword) == list:
                            for word in keyword:
                                word = keyword.lower()
                                filename = file.lower()
                                try:
                                    if word in filename:
                                        os.rename(file,newname + category_code + f'{i}' + ext)
                                except:
                                    print(f'File under the name {newname+i+ext} already exist line 637')
                    
                        elif type(keyword) == str:
                            word = keyword.lower()
                            filename = file.lower()
                            try:
                                if word in filename:
                                    os.rename(file,newname + category_code + f'{i}' + ext)
                            except:
                                print(f'File under the name {newname+i+ext} already exist line 648')
                    except:
                        print('This name already exist')
        except:
            print('Invalid type. Multiple must be of type int or bool line 686')

        print('Done')
    
# move to different file
    def contains(self, patterns, text, remove_numbers = False):
        ''' returns true if the pattern is in the text and false otherwise 
        
        parameters
        ----------
        patterns -> string or iterable (not dict):
            - tells the function what to identify in the "text" string

        text -> string:
            - The text that you want to try and find the "patterns" in

        remove_numbers -> bool:
            determines whether or not the numbers will be removed from the text
            before the pattern is searched for   
        '''
        if remove_numbers:
            text = re.sub('[0-9]', '', text)

        if patterns == "":
            return False

        elif type(patterns) != str:
            matches = []
            for pattern in patterns:
                text, pattern = text.lower(), pattern.lower()
                match = re.search(pattern, text)
                if match:
                    matches.append(True)
                else:
                    matches.append(False)
            
            if any(matches):
                return True
            else:
                return False
                
        else:
            # convert both the text and the pattern to lowercase
            text, pattern = text.lower(), patterns.lower()
                
            match = re.search(pattern, text)
            if match:
                return True
            else:
                return False

    def path_contains(self, pattern, text, degree = 3, verbose = False):
        ''' same as contains but used for paths only '''
        # make all the text lowercase 
        text, pattern = text.lower(), pattern.lower()

        # split the path into individual sections and return as a string
        #split = str(text.split('\\')[-degree:])
        sections = text.split('\\')[-degree:]
        
        
        # search for the pattern in the path
        
        for index, section in enumerate(sections):
            match = re.search(pattern, section)
            #print(section)
            if match:
                if verbose:
                    print(f"Sections using a degree of {degree}: {sections}")
                    print(f'{pattern} is in {text}.')
                    print(f'The pattern was found in section {index+1}: {section}')
                return True
            else:
                if verbose:
                    print(f'{pattern} is not in {text}')
                    #print(f"Sections using a degree of {degree}: {sections}")
            
        return False
        
        
        


