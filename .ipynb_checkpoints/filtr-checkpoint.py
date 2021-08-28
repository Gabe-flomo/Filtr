import os
import random 
import shutil
#import spacy as nlp
import time
import concurrent.futures as future
from multiprocessing import Process
import queue
import wave


class Filtr():

    def __init__(self,path,dest = "D:\\Documents\\Dest\\Filtr\\Class test files"):
        """ initializes the class with current path"""

        # sets the path passed into the constructor as the current working path
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

    def __newpath__(self,name):
        return os.path.join(self.current_path,name)

    def __update__(self):
        os.chdir(self.current_path)
        self.current_files = self.files(self.current_path)
        self.current_folders = self.folders(self.current_path)
        self.working_directory = os.getcwd()

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

    def files(self,path = None):
        """This function lists only the files in a path and 
        exludes the directories and returns a list of the files"""

        
        dirs = []
        if path is not None:
            with os.scandir(path) as files:
                for file in files:
                    if not file.name.startswith(".") and file.is_file():
                        dirs.append(file.name)
            self.current_files = dirs
            return dirs
        else:
            with os.scandir() as files:
                for file in files:
                    if not file.name.startswith(".") and file.is_file():
                        dirs.append(file.name)
            self.current_files = dirs
            return dirs

    def output(self,text,path = None,ext = False,ignore = None, reject = False):
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
        duration = self.duration()

        # Filter files and output
        if text == ("files" or "file"):
            file_list = self.files() if path is None else self.files(path)
            ignore = tuple(ignore) if ignore is not None else ignore

            filtered = []
            if len(file_list) == 0:
                print("There are no files in this location")
            else:   
            # loop through files and check for conditions
                for file in file_list:

                    # condition 1         #
                    # dont show extension #
                    # show all files      #
                    # dont remove         #               
                    if (ext == False) and (ignore == None) and (reject == False):
                        file = os.path.splitext(file)
                        filtered.append(file[0])

                    # condition 2                                   #
                    # dont show extension                           #    
                    # show all files except for the ignored ones    #
                    # dont remove                                   #
                    elif (ext == False) and (ignore is not None) and (reject == False):
                        file = ["",""] if file.endswith(ignore) else os.path.splitext(file)
                        filtered.append(file[0])


                    # condition 3
                    # dont show extension
                    # show all files except for the ignored ones
                    # remove ignored files
                    elif (ext == False) and (ignore != None) and (reject == True):
                        
                        if file.endswith(ignore):
                            os.remove(file)
                        
                        else:
                            file = ["",""] if file.endswith(ignore) else os.path.splitext(file)
                            filtered.append(file[0])


                    # condition 4
                    # show extension
                    # show all files except for the ignored ones
                    # dont remove
                    elif (ext == True) and (ignore != None) and (reject == False):
                        file = "" if file.endswith(ignore) else file
                        filtered.append(file)
                    

                    # condition 5
                    # show extension
                    # show all files except for the ignored ones
                    # remove ignored files
                    elif (ext == True) and (ignore != None) and (reject == True):
                        if file.endswith(ignore):
                            os.remove(file)
                            file = ""
                            filtered.append(file)
                        
                        else:
                            filtered.append(file)


                    # condition 6
                    # show extension
                    # show all files 
                    # keep all
                    elif (ext == True) and (ignore == None) and (reject == False):
                        filtered.append(file)    

            width = max(len(f) for f in filtered) + 4

            # output files
            print("Name\t\t\t\tDuration")
            print("----\t\t\t\t--------\n")
            for count,file in enumerate(filtered):
                padding = width - len(file)
                space = " " * padding
                if (duration[count] <= 60):
                    print(f"{count+1}) {file} {space} {round(duration[count],2)}")
                elif duration[count] > 60:
                    mins = duration[count] // 60
                    secs = duration[count] % 60
                    print(f"{count+1}) {file} {space} {mins}:{secs}")
                             

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
            for count,file in enumerate(files):
                print(f"{x+1}) {file}")
                x += 1
        
        print()
           
    def xfer(self,file,dest = None):
        t1 = time.perf_counter()
        if dest is None:
            dest = self.current_destination
            if type(file) == list:
                for i in file:
                    shutil.copy(i,dest)
            else:  
                shutil.copy(file,dest)
        else:
            shutil.copy(file,dest)

        t2 = time.perf_counter()
        finish = t2-t1
        print(f'finished in {round(finish,2)} seconds')
        return "Moved"

    def process(self, workers = os.cpu_count()):
        """Counts how many logical processors there are on the machine and uses that number
        to determine how many queues to create. Each queue will get a portion of the total number 
        of files in the current directory (files_per_queue = total_files / number_of_processors). 

        Each queue is then assigned to a process and the files in that queue will be moved within
        that process.

        ---------------------------------------
        Parameters 
        ---------------------------------------

         workers:

         determines the number processors to use, if nothing is given it will default to the maximum
         number.

         """

        t1 = time.perf_counter()
        num_cpu = workers
        processes = []
        q = self.get_queues(workers)
                
        for i in range(num_cpu):
            #print(i)
            target = q[i].get()
            p = Process(target = self.xfer, args=[target])
            processes.append(p)

        for p in processes:
            p.start()

        for p in processes:
            p.join()

        
   

        t2 = time.perf_counter()
        finish = t2-t1

        print(f'finished in {round(finish,2)} seconds')

    def get_queues(self,workers = os.cpu_count()):

        q = queue.Queue()
        num_cpu = workers
        #print(f"CPUS: {num_cpu}")

        files = self.current_files
        num_files = len(files)
        #print(f"FILES: {num_files}")

        if num_files <= num_cpu * 2:
            quo = len(files)
        else:
            quo = num_files // num_cpu
            rmd = num_files % num_cpu

        #print(f"quotient: {quo}")
        #print(f"remainder: {rmd}")

        queues = []
        files_left = num_files

        while files_left > 0:
            filelist = []
            if files_left == rmd:
                #print(f"files left: {files_left}")
                for _ in range(files_left):
                    #print(f"len: {len(files)}, position: {i}")
                    file = files.pop()
                    filelist.append(file)

                #print(f"filelist: {filelist}")
                q.put(filelist)
                queues.append(q)
                files_left -= rmd
                

            else:
                #print(f"files left: {files_left}")
                for i in range(quo):
                    file = files.pop()
                    filelist.append(file)

                q.put(filelist)
                
                queues.append(q)
                files_left -= quo
                

        print(f"there are {len(queues)} queues")
        return queues

    def open(self,index):
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
        
    def duration(self,path = None):
        """
        function that will return the duration of a file
        """

        files = self.files(path) if path is not None else self.files()
        durations = []
        for file in files:
            try:
                with wave.open(file,'r') as audio:
                    frate = audio.getframerate()
                    nframes = audio.getnframes()
                    duration = nframes/frate
                    durations.append(duration)
            except:
                print(f"The File: {file} is an unsupported type and \nits duration could not be calculated.\n")
                duration = 0
                durations.append(duration)

        return durations

        
            