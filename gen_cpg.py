
import os
from util.fileUtil import getListOfFiles, write_list_to_txt2, read_txt, copy_files
from subprocess import call, run

def main():
        # the path of project under test. If you want to analyze a different project for potential mutations
    # provide a different address

    # the name of the project
    sut = 'tensorflow'

    target_path = '/media/nimashiri/SSD/'+sut+'/tensorflow/core/kernels'

    source_files_in_one_place = '/media/nimashiri/SSD/'+sut+'_source_files_path'

    # please indicate the location where you want to store all generated cpgs
    #cpg_dest_path = '/home/nimashiri/'+sut+'_cpg_path'

    # if not os.path.exists(cpg_dest_path):
    #     os.makedirs(cpg_dest_path)


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