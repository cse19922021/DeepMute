import os
import re
import os, shutil
from util.DBadaptor import DBHandler
from subprocess import call
import argparse
import re, sys
from util.fileUtil import read_code_file, read_txt, copy_files, getListOfFiles, write_list_to_txt2
from multiprocessing import Pool

if os.path.isfile('./mutation_database.db'):
    db_obj = DBHandler(False)
else:
    db_obj = DBHandler(True)


def handle_source_files(target_path):

    source_files_in_one_place = './temp'

    if not os.path.exists(source_files_in_one_place):
        os.makedirs(source_files_in_one_place)

    if not os.path.isfile('./projects_files.txt'):
        # get list of all files
        _files = getListOfFiles(target_path)
        # output the list to disk
        write_list_to_txt2(_files)
        
    # read list of all files from disk
    fname = 'projects_files.txt'
    _files = read_txt(fname)

    copy_files(_files, source_files_in_one_place)


class CheckPotential:
    def __init__(self) -> None:
        self._method = ""
        self.REDAWN = 0
        self.mutId = 0

    def reset_flag(self):
        self.line_reg = []

    def get(self):
        return self._method

    def set(self, _input):
        self._method = _input

    def rangeCheck(self, line):
        for l in range(line, len(self._method)):
            #print(self._method[l])
            if re.findall(r'[;]', self._method[l]):
                return l
    
    def integer_overflow_potential(self, current_file):
        print(current_file)
        for line in self._method:
            if self._method[line] != '':
                self.mutId += 1
                check1 = re.findall(r'\bint64\b', self._method[line])
                check2 = re.findall(r'\buint32_t\b', self._method[line])
                check3 = re.findall(r'\bint64_t\b', self._method[line])
                check4 = re.findall(r'\bsize_t\b', self._method[line])
                if check1 or check2 or check3 or check4:
                    db_obj.insert_data(self.mutId,line, line, self._method[line], '', os.path.basename(current_file), "numericalPrecision", current_file, '')


    def tensor_property_checker(self, current_file):
        print(current_file)
        for line in self._method:
            if self._method[line] != '':
                self.mutId += 1
                check1 = re.findall(r'\bOP_REQUIRES_OK\b\s*\(([^\)]+)\)', self._method[line])
                check2 = re.findall(r'\bOP_REQUIRES\b\s*\(([^\)]+)\)', self._method[line])
                if check1 or check2:
                    stmt = []
                    end_line = self.rangeCheck(line)
                    for sub_line in range(line, end_line+1):
                        stmt.append(self._method[sub_line])
                    stmt = ''.join(stmt)
                    db_obj.insert_data(self.mutId,line, end_line, stmt, '', os.path.basename(current_file), "OP_REQUIRE", current_file, '')

    def apply(self, current_file):
        with Pool(10) as p:
            p.map(self.tensor_property_checker, (current_file,))

visited = set()        

def regex_parser(str):
    return re.findall(r'\bOP_REQUIRE\b\s*\(([^\)]+)\)', str)

def parse_ast(tree):
    print(tree['code'])
    if tree == None:
        return 1
    if not tree['has_child']:
        return 1
    if tree['id'] not in visited:
        visited.add(tree['id'])
    for neighbors in tree['children']:
        parse_ast(neighbors)

def parse_addr(f):
    for com in f.split('/'):
        if com == 'core':
            if com == 'kernels':
                return True
            else:
                return False

def main(args):
    handle_source_files(args.target_path)
    _obj = CheckPotential()

    fname = 'projects_files.txt'
    _files = read_txt(fname)
    for f in _files:
        fname = os.path.basename(f)
        if re.findall(r'(\bcore\/kernels\b)', f):
            data_dict = read_code_file(f)
            _obj.set(data_dict)
            _obj.apply(f)
            _obj.reset_flag()
    

if __name__ == '__main__':

    Epilog  = """usage: python analyze.py --target_path=../tensorflow/tensorflow/core/kernels/"""

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description='Analyze tensorflow for potential mutations.', epilog=Epilog)

    parser.add_argument('--target_path' , type=str, help='Please enter the path where you have cloned tensorflow source files.')

    args = parser.parse_args()

    if args.target_path == None:
        parser.print_help()
        sys.exit(-1)

    main(args)
    shutil.rmtree('./temp')