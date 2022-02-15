
import os
from util.fileUtil import write_list_to_txt3
import sys
import argparse


def getListOfFiles(dirName):
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

def main(args):
    if not os.path.isfile('./kernel_tests_files.txt'):
        # get list of all files
        _files = getListOfFiles(args.target_path)
        # output the list to disk
        
        write_list_to_txt3(_files)
        

if __name__ == '__main__':
    Epilog  = """usage: python get_tests_list.py --target_path=../tensorflow/tensorflow/python/kernel_tests/"""

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Get list of all kernel test files from tensorflow.', epilog=Epilog)

    parser.add_argument('--target_path' , type=str, help='Please enter the path of tensorflow kernel test files.')

    args = parser.parse_args()

    if args.target_path == None:
        parser.print_help()
        sys.exit(-1)

    main(args)