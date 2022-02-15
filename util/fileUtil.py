import os, shutil
from pathlib import Path
import codecs
import pickle, csv

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
    # if lang == 'C':
    #     allFiles = filter(allFiles)
    # else:
    allFiles = filter(allFiles)
    return allFiles

def filter_python_tests(target_files):
    filtered = []
    for f in target_files:
        if 'test' in f:
            if f.endswith('.py'):
                filtered.append(f)
    return filtered

def filter(target_files):
    filtered = []
    for f in target_files:
        if 'test' not in f:
            if f.endswith('.c') or f.endswith('.cc') or f.endswith('.cpp'):
                filtered.append(f)
    return filtered

def copy_files(c_only, dst):
    for f in c_only:
        shutil.copy2(f, dst)

def read_csv(csv_file_path):
    data = []
    with open(csv_file_path) as fp:
        header = fp.readline()
        header = header.strip()
        h_parts = [hp.strip() for hp in header.split('\t')]
        for line in fp:
            line = line.strip()
            instance = {}
            lparts = line.split('\t')
            for i, hp in enumerate(h_parts):
                if i < len(lparts):
                    content = lparts[i].strip()
                else:
                    content = ''
                instance[hp] = content
            data.append(instance)
        return data


def buildWrite(methodName):
    with codecs.open(methodName, 'w') as f_method:
        for line in _method:
            f_method.write("%s\n" % self._method[line])
        f_method.close()

def read_code_file(file_path):
    code_lines = {}
    file_path = Path(file_path)
    if file_path.exists:
        with open(file_path) as fp:
            for ln, line in enumerate(fp):
                assert isinstance(line, str)
                line = line.strip()
                if '//' in line:
                    line = line[:line.index('//')]
                code_lines[ln + 1] = line
    return code_lines

def write_to_disc(filecontent, target_path):
    with codecs.open(target_path, 'w') as f_method:
        for line in filecontent:
            f_method.write("%s\n" % filecontent[line])
        f_method.close()


def read_entire_code_file(file_path):
    with open(file_path, 'r') as content_file:
        content_list = content_file.r
    return content_list

def read_txt(fname):
    with open(fname, 'r') as fileReader:
        data = fileReader.read().splitlines()
    return data

def write_list_to_txt2(data):
    with open("projects_files.txt", "a") as file:
        for row in data:
            file.write(row+'\n')

def write_list_to_txt3(data):
    with open("kernel_tests_files.txt", "a") as file:
        for row in data:
            file.write(row+'\n')

def write_list_to_txt(data, project_name):
    with open(project_name, "a") as file:
        #for row in data:
        file.write(str(data)+'\n')


def csv_writer(data, filename):
    with open(filename+'.csv', 'a', newline='\n') as myfile:
        wr = csv.writer(myfile)
        wr.writerow(data)