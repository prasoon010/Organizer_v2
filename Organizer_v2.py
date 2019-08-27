import os
import hashlib
import yaml
import sys

new_dict = {}
failed_list = []

#function to find the md5 hash of a given file

def getmd5(file=None):
    md5obj = hashlib.md5()
    CHUNK = 1024000
    if file and os.path.exists(file) and os.path.isfile(file):
        with open(file,'rb') as fh:
            while True:
                data = fh.read(CHUNK)
                if data:
                    md5obj.update(data)
                else:
                    break
        return md5obj.hexdigest()
    
#function creating folders for different file types

def makefolder(download_dir,folders):
    for folder in folders: 
        abs_dir = os.path.join(download_dir,folder) #stores absolute path
        if not os.path.exists(abs_dir):     #creates folders if does not exists at destination
            os.mkdir(abs_dir)



def movefiles(movefile,download_dir,new_dict):
    
    ext = movefile.split('.')[-1]   #stores extension of file name
    if ext in new_dict.keys():   #membership check
        source_dir = os.path.join(download_dir,movefile) #stores full path of source file
        dest_dir = os.path.join(download_dir,new_dict[ext],movefile)  #stores full path of destination file
        if not os.path.isfile(dest_dir):
            os.rename(source_dir,dest_dir)   #moves file if not exists at destination directory
            return True
            
            #Following condition check if file with same name exists in destination
            
        elif os.path.isfile(dest_dir) and os.path.getsize(source_dir) == os.path.getsize(dest_dir):
            if getmd5(source_dir) == getmd5(dest_dir):
                os.remove(source_dir)   #if files at source and destination are same, deletes the file from source
                return True
            else:
                print('Moving file {} failed: same filename exists at {}'.format(movefile,dest_dir))
                return False
        else:
            print('Moving file {} failed: same filename exists at {}'.format(movefile,dest_dir))
            return False



def main():
    m = 0
    f = 0
    
    try:
        with open('FileExt.yml','r') as fh:
            file_ext = yaml.load(fh)   # file_ext is type dict which will contain Foldername as keys and corresponding list of file extensions value
    except:
        print('Yaml parse error: check file: Fileext.yml')
        sys.exit(1)
   
    
    download_dir = input('Enter the download directory path: ')
    download_files = os.listdir(download_dir)
    
    for value in file_ext.keys():
        for item in file_ext[value]:
            new_dict[item] = value    # the dict new_dict will store file extension as key and folder name as value
    folders = list(set(new_dict.values())) #save uniq list of  folder name
        
    makefolder(download_dir,folders)  #download_dir - Download directory, file_ext - dictionary mentioned earlier

    for movefile in download_files:
        file = os.path.join(download_dir,movefile) #file - stores full path of files in download directory
        if os.path.isfile(file):        #checking if it is a file
            
 #Moving files to corresponding folders and counting the success/fail moves

            if movefiles(movefile,download_dir,new_dict): #movefile - stores filenames in the download directory
                m += 1
            else:
                f += 1
                failed_list.append(movefile)
            
 #prints the total success and failed condition  

    print('Total files moved: {}, Total failed: {}'.format(m,f))
    if f > 0:
        i = input('Enter "l" to print failed list:  ')
        if i == 'l':
            for listed in failed_list:
                print(listed)           

if __name__ == '__main__':    #import guard
    main()
else:
    print('Organizer cannot be imported')
    sys.exit()
