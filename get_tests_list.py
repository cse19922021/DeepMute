
import os
from util.fileUtil import write_list_to_txt2


def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    allFiles = filter_python_tests(allFiles)
    return allFiles

def filter_python_tests(target_files):
    filtered = []
    for f in target_files:
        if 'test' in f:
            if f.endswith('.py'):
                filtered.append(f)
    return filtered

def main():
        # the path of project under test. If you want to analyze a different project for potential mutations
    # provide a different address

    # the name of the project
    sut = 'tensorflow'

    # Please do not change the second part of the address. 
    target_path = '/path/to/tensorflow/source/files/'+sut+'/tensorflow/python/kernel_tests'

    out_file_name = 'tensorflow_kernel_test'

    # we need list of all files from project under test to check for potential mutatioons
    # please note that we only extract C and CC files since this tool solely designed to 
    # analyze programs or projects written in C or CC. 
    if not os.path.isfile('./'+out_file_name+'_files.txt'):
        # get list of all files
        _files = getListOfFiles(target_path)
        # output the list to disk
        write_list_to_txt2(_files, out_file_name)
        
    
    # read list of all files from disk
    #_files = read_txt(sut)

if __name__ == '__main__':
    main()