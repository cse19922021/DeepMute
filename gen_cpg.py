
import os
from util.fileUtil import getListOfFiles, write_list_to_txt2, read_txt, copy_files
import argparse

def main():
    # the path of project under test. If you want to analyze a different project for potential mutations
    # provide a different address

    # the name of the project
    sut = 'tensorflow'

    # please do not remove 'sut' from the address
    target_path = '/path/to/'+sut+'/tensorflow/core/kernels'

    # please do not remove 'sut' from the address
    source_files_in_one_place = '/path/to/folder/where/we/want/to/extract/'+sut+'all/kernel/files'

    if not os.path.exists(source_files_in_one_place):
        os.makedirs(source_files_in_one_place)

    # we need list of all files from project under test to check for potential mutatioons
    # please note that we only extract C and CC files since this tool solely designed to 
    # analyze programs or projects written in C or CC. 
    if not os.path.isfile('./'+sut+'_files.txt'):
        # get list of all files
        _files = getListOfFiles(target_path)
        # output the list to disk
        write_list_to_txt2(_files, sut)
        
    # read list of all files from disk
    _files = read_txt(sut)

    copy_files(_files, source_files_in_one_place)

    #run('./scripts/generate_cpgs.sh')

if __name__ == '__main__':
    main()