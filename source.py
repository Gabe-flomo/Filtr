from Filtr.filtr import Filtr
import os
import time


# when running multiprocessing you must use this syntax
'''if __name__ == '__main__':
    path = 'D:\\Samples\\Test\\Unsifted\\2019\\process'
    f = Filtr(path)
    f.output("files")
    f.process(workers = 4)
    \00 - Loops
    
'''


if __name__ == '__main__':
    path = r'E:\Sample library\Spring\Samplified Packs'
    #path = r'E:'
    f = Filtr(path = path)
    #f.filetree(ignore='.asd', reject=True, sortby='name')
    #f.viewrecords()
    ignore = ('.mid', '.asd', '.DS_Store', '.txt', '.zip', '.mp3', '.nki', '.ogg', '.peak',
              '.nksn', '.jpg', '.fxb', '.fxp', '.aiff', '.nmsv', '.aif', '.adg', '.midi', '.ffp', '.xmp', '._')
    #f._save_records(path = r'E:\Sample library',ignore = ignore)
    # print(f._load_records())

    
    path_drums = (r'E:\Sample library\Spring', r'E:\Sample library\1',
                  r'E:\Sample library\All Sounds', r'E:\Sample library\2')

    path_inst = (r'E:\Sample library\All Sounds\instrument',
                 r'E:\Sample library\All Sounds',
                 r'E:\Sample library\2')

    path_eltr = (r'E:\Sample library\All Sounds\ambiance',
                 r'E:\Sample library\All Sounds\FX', r'E:\Sample library\All Sounds\December', r'E:\Sample library\2',
                 r'E:\Sample library\All Sounds')

    path_world = (r'E:\Sample library\All Sounds',
                  r'E:\Sample library\2\Cymatics - LIFE Ambient Recordings - Pt 1',)

    ignore = ('.mid', '.asd', '.DS_Store', '.txt', '.zip', '.mp3', '.nki', '.ogg', '.peak',
    '.nksn','.jpg','.fxb','.fxp','.aiff','.nmsv','.aif','.adg','.midi','.ffp','.xmp','._')
    ban = ['impact', '__MACOSX','vox','arp']
    dest = r'E:\Documents\My Projects\Filtr\Data\Audio\Synth'

    start = time.perf_counter()
    f.generate('synth', dest=dest, datalimit=1200, ignore=ignore, ban=ban, verbose = True, degree = 3,verify = True)
    #f.path_contains('bounce',path,3,verbose = True)
    end = time.perf_counter()
    print(f"finished in {end - start} seconds")
    # print(f.contains(['loop','gas'],'this is a kick loop'))
   
    











#files = f.files(ignore = '.asd')
#f.output("files", ignore = '.asd')
#f.class_info()

#f.generate_data('kick', data_limit=5, path=path, dest=r'E:\Documents\My Projects\Filtr\Data\Audio\Synth', duration_limit = 10)
#f.rename('snare','sample',category_code='DS',path="D:\\Documents\\Atom\\myrepos\\Filtr\\Filtr\\Audio\\Snare")
#index = input("Enter the index: ")
#index = int(index) if index.isnumeric() else index
#f.open(index)
#path = f.current_path
#print(f"getting info for: {os.path.basename(path)}\n")
#f.class_info()
#files = f.files()
#f.xfer(files)
#print(f.duration())'''



