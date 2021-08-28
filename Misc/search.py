import os 
import shutil
from time import *
import winsound

def has_subdirs(path):
    """ This returns true if the path has subdirectories in it
    if there are none it will return false """
    directories = list_directories(path)
    if len(directories) == 0:
        return False
    elif len(directories) > 0:
        return True

def has_sub_deep( path ):
    """This function checks to see if a directory has sub-directoies all the way
    down to the last directory with subdrectories in it"""

    ## creates a list with all the entries in the path
    dirs = os.listdir(path)
       
    file_count = 0
    for i in range(len(dirs)): 
        ## this means there were no sub-directories
        if len(dirs) == 0: 
            print("there were none")
            return False

        ## for each entry create a temporary path  
        temp_path = os.path.join(path,dirs[i])

         ## check if that path is a directory, if so look deeper
        if os.path.isdir(temp_path):
                print("This is a directory",temp_path)
                return has_sub_deep(temp_path)
                
        ## Checks if the path is a file
        elif os.path.isfile(temp_path):
            file_count += 1
            ##print("file found at location",file_count,temp_path)
            if i == len(dirs)-1:
                temp_path = path_step(temp_path)
                return temp_path

def list_directories(path):
    """This function lists only the directories in a path and 
    exludes the files and returns a list of the directories"""

    ## creates a list with all the entries in the path
    dirs_inpath = os.listdir(path)
    dirs = []


    for i in range(len(dirs_inpath)):
        ## for each entry create a temporary path  
        temp_path = os.path.join(path,dirs_inpath[i])

         ## check if that path is a directory
        if os.path.isdir(temp_path):
            dirs.append(dirs_inpath[i])
    
    return dirs

def matching(path,keyword):
    """This function is used if there are multiple keywords and
    you would like to see if any of the keywords matches the name
    of a directory in your path
    
    for example:
        directory = ["this","is","an","example"]
        keyword = ["example","this"]
        are keyword in directory"""

    ### creates a list of the directories 
    main_dir = list_directories(path)
    for i in range(len(main_dir)):
        main_dir[i] = main_dir[i].lower()

    found = []

    """ starts with the first entry in the directory and chacks if any 
    of the keywords match the directory name """

    for i in range(len(main_dir)):
        for j in range(len(keyword)):
            if keyword[j] in main_dir[i]:
                found.append(main_dir[i])
    
    for word in found:
        times = found.count(word)
        if times > 1:
            found.remove(word)


    ## returns a list of the matches its found
    return found

def match(path,keyword):
    """ Use this function if you want to check
    for a match with a single key word.
    
    for example:
        directory = ["this","is","an","example"]
        keyword = "example"
        is keyword in directory """

    main_dir = list_directories(path)
    
    word_count = 0
    found = []
    for i in range(len(main_dir)):
        if keyword in main_dir[i]:
            word_count += 1
            found.append(main_dir[i])
    
    for word in found:
        times = found.count(word)
        if times > 1:
            found.remove(word)

def path_step(path,cutoff = 1):
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

def create_path(words,path):
    "takes in a list and a path and creates a path for each keyword in the list"
    
    pathlist = []

    for i in range(len(words)):
        temp = os.path.join(path,words[i])
        pathlist.append(temp)
    
    return pathlist

def formatdir(dirs):
    for i in range(len(dirs)):
                print(i+1,dirs[i],sep = ") ")
    print()

def change_lower(path,keywords):
    """This function takes in a path and looks at all the directories in it
    and changes them to lowercase. """
    
    paths = create_path(keywords,path)
    for i in range(len(paths)):
        base = os.path.basename(paths[i])
    
def createpath(index,folders,path):
    "takes in a index, list of folders, and the original path and creates paths for each folder"
    
    pathlist = []

    for i in index:
        temp = os.path.join(path,folders[i-1])
        pathlist.append(temp)
    
    return pathlist
 
def clear():
    os.system('cls')

def wait():
    sleep(2)

def move_dir(transfers,dest):

    for path in transfers:
        base = os.path.basename(path)
        check = os.path.join(dest, base)
        if os.path.exists(check):
            print("This directory already exists in the destination, so it will be removed from the source. ")
            try:
                shutil.rmtree(path)
            except (PermissionError,OSError):
                print("This directory could not be deleted and you'll have to do it manually. ")
        else:
            try:
                shutil.move(path,dest)
            except (PermissionError,OSError):
                print("An error may have occured and were trying to find a solution")
                base = os.path.basename(path)
                check = os.path.join(dest,base)
                if os.path.exists(check):
                    print("It looks like this directory has been moved but it may still exist in its original location")

    print("done")
    wait()

def get_base(paths):
    baselist = []
    for path in paths:
        
        baselist.append(os.path.basename(path))
    return baselist

def current_folder(path):
    """this function takes in a path and displays the folder
    that your currently working in"""

    folder = os.path.basename(path)
    return folder

def move_files(path,dest):
    """Checks to see if a path has any files and if it does ask the user if they would like to see them"""
   
    ## creates a list with all the entries in the path
    dirs_inpath = os.listdir(path)
    files = []


    for i in range(len(dirs_inpath)):
        ## for each entry create a temporary path  
        temp_path = os.path.join(path,dirs_inpath[i])

         ## check if that path is a file
        if os.path.isfile(temp_path):
            files.append(dirs_inpath[i])

    resp = input("select the files to move using this format:'14-16'. ")
    sections = resp.split("-")
    start = sections[0]
    finish = sections[1]
    start = int(start)
    x = start
    finish = int(finish)
    while start<=finish:
            file_path = os.path.join(path,files[start-1])
            shutil.move(file_path,dest)
            start += 1
    print((finish-x)+1,"Files have been moved.")
    wait()

def check_files(path):
    ## creates a list with all the entries in the path
    dirs_inpath = os.listdir(path)
    files = []

    for i in range(len(dirs_inpath)):
        ## for each entry create a temporary path
        temp_path = os.path.join(path, dirs_inpath[i])

        ## check if that path is a directory
        if os.path.isfile(temp_path):
            files.append(dirs_inpath[i])

        if len(files) == 0:
            return False
        elif len(files) > 1:
            return True


def create_alternate_path(choice,dirs_inpath,current_path):
    """takes in the index as the choice and locates the directory at that 
    index, then adds it onto the current path aka the essential path"""

    newpath = os.path.join(current_path,dirs_inpath[choice-1])
    return newpath

def playsound(audio,path):
    os.chdir(path)
    #start = time.time()
    #winsound.PlaySound(audio,winsound.SND_FILENAME|winsound.SND_ASYNC)
    winsound.PlaySound(audio, winsound.SND_FILENAME | winsound.SND_ASYNC)

def previewSound(index,path):

    dirs_inpath = os.listdir(path)
    files = []

    for i in range(len(dirs_inpath)):
        ## for each entry create a temporary path
        temp_path = os.path.join(path, dirs_inpath[i])

        ## check if that path is a directory
        if os.path.isfile(temp_path):
            files.append(dirs_inpath[i])

    audio = files[index-1]
    playsound(audio,path)

def list_files(path):
    fileList = os.listdir(path)
    files = []

    for file in fileList:
        if file.endswith(".asd"):
            temp = os.path.join(path,file)
            os.remove(temp)

    for i in range(len(fileList)):
        ## for each entry create a temporary path
        temp_path = os.path.join(path, fileList[i])

            ## check if that path is a file
        if os.path.isfile(temp_path):
             files.append(fileList[i])

    return files

def getSound(index,path):

    dirs_inpath = os.listdir(path)
    files = []

    for i in range(len(dirs_inpath)):
        ## for each entry create a temporary path
        temp_path = os.path.join(path, dirs_inpath[i])

        ## check if that path is a directory
        if os.path.isfile(temp_path):
            files.append(dirs_inpath[i])

    audio = files[index-1]
    return audio

'''for i in range(len(dirs)): 
            ## this means there were no sub-directories
            if len(dirs) == 0: 
                print("there were none")
                return False

            ## for each entry create a temporary path  
            temp_path = os.path.join(path,dirs[i])

            ## check if that path is a directory, if so look deeper
            if os.path.isdir(temp_path):
                    print("This is a directory",temp_path)
                    return self.__info__(temp_path)
                    
            ## Checks if the path is a file
            elif os.path.isfile(temp_path):
                file_count += 1
                ##print("file found at location",file_count,temp_path)
                if i == len(dirs)-1:
                    temp_path = self.path_step(temp_path)
                    return temp_path'''
