import os
import search as s

# creating a hard link
# first list the directories in the path

import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # Code of your program here
     while True:
        default = "D:\\Documents\\Test Files"
        path = input("Enter your path or type default.")
        


        if path == "default":
            dirs = s.list_directories(default)

            s.formatdir(dirs)
        else:
            print("Directories:\n")
            dirs = s.list_directories(path)
            s.formatdir(dirs)
            print()
            print("Files:\n")
            d = s.list_files(path)
            s.formatdir(d)

        ans = input("open to open, slnk for soft link, hlnk for hard link, skip to retun: ")

        if ans == "open":
            files = s.list_files(path)
            print(files)
            print()
            x = eval(input("The file at index "))
            files = os.path.join(path,files[x-1])
            f = open(files,"r")
            contents = f.read()
            print(contents)
            f.close()
            cont = input("press anything to continue.")
        
        elif ans == "slnk":
            files = s.list_files(path)
            print(files)
            print()
            x = eval(input("The file at index "))
            files = os.path.join(path,files[x-1])
            os.symlink(files,"D:\\Documents\\Dest")
            print("link has been created.")
            print()
            cont = input("press anything to continue.")

        elif ans == "hlnk":
            files = s.list_files(path)
            print(files)
            print()
            x = eval(input("The file at index "))
            files = os.path.join(path,files[x-1])
            os.link(files,"D:\\Documents\\Dest\\Hard")
            print("link has been created.")
            print()
            cont = input("press anything to continue.")
            print("admin")
    

   
   
    #ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

