import shutil
from tabnanny import check
import threading
from util.DBadaptor import DBHandler
from util.fileUtil import copy_files, csv_writer, read_code_file, read_csv, read_txt, write_to_disc, write_list_to_txt, write_list_to_txt2
from subprocess import call, check_call, run
import subprocess, multiprocessing
import re, os
from threading import Thread
from multiprocessing import Pool
import pandas as pd
from datetime import datetime
import time, random

all_run = []

valid_tests = 'tensorflow_kernel_test_all_run'


if os.path.isfile('./mutation_database.db'):
    db_obj = DBHandler(False)
else:
    db_obj = DBHandler(True)

def process(input_addr, filename):
    file_i = os.path.basename(filename)
        #print('Total number of executed unit tests: {}'.format(i))
    #print("executed {}. thread".format(input_addr))
        #if not event.set():
    try:
        command = 'python3 '+input_addr
        result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        msg, err = result.communicate()
        if msg.decode('utf-8') != '':
            stat, logging = parse_shell(msg.decode('utf-8'))
            if stat:
                csv_writer([input_addr,True], 'test_status')
                write_list_to_txt(logging, './logging/'+filename+'/'+file_i)
            else:
                csv_writer([input_addr, False], 'test_status')
                write_list_to_txt(logging, './logging/'+filename+'/'+file_i)
        else:
            stat, logging = parse_shell(err)                
            if stat:
                csv_writer([input_addr, True], 'test_status')
                write_list_to_txt(logging, './logging/'+filename+'/'+file_i)
            else:
                csv_writer([input_addr, False], 'test_status')
                write_list_to_txt(logging, './logging/'+filename+'/'+file_i)
    except Exception as e:
        print("thread.\nMessage:{1}".format(e))

def process_prerun(input_addr):
    print("executed {}. thread".format(input_addr))
    command = 'python3 '+input_addr
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    msg, err = result.communicate()
    if msg.decode('utf-8') != '':
        stat = parse_shell(msg.decode('utf-8'))
        if stat:
            print('Test Failed')
        else:
            write_list_to_txt(input_addr, valid_tests)
    else:
        stat = parse_shell(err)                
        if stat:
            print('Test Failed')
        else:
            write_list_to_txt(input_addr, valid_tests)
    

class KillableThread(Thread):
    def __init__(self, sleep_interval, input_addr):
        super().__init__()
        self._kill = threading.Event()
        self._interval = sleep_interval
        self.input_addr = input_addr

    def run(self):
        while True:
            process(self.input_addr)

            # If no kill signal is set, sleep for the interval,
            # If kill signal comes in while sleeping, immediately
            #  wake up and handle
            is_killed = self._kill.wait(self._interval)
            if is_killed:
                break

        print("Killing Thread")

    def kill(self):
        self._kill.set()

def getListOfFiles2(dirName):
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
            allFiles = allFiles + getListOfFiles2(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles

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

def filter(target_files):
    filtered = []
    for f in target_files:
        if 'test' not in f:
            if f.endswith('.c') or f.endswith('.cc') or f.endswith('.cpp'):
                filtered.append(f)
    return filtered

def filter_test_files(test_files, target):
    file_name = os.path.basename(target)
    # parent_dir = os.path.dirname(target)
    # parent_dir = parent_dir.split('/')[-1]
    x = file_name.split('.')
    f = x[0]+'_'+'test'
    f = f +'.'+'py'
    root_test_path = '/media/nimashiri/SSD/tensorflow/tensorflow/python/kernel_tests'
    for root, dir, files in os.walk(root_test_path):
        matches = [match for match in files if f in match]
        if matches:
            return root+'/'+matches[0]
    
    for t in test_files:
        s = t.split('/')
    pass


def search_for_file(filename):
    src = ''
    # all_files = getListOfFiles('/media/nimashiri/SSD/tensorflow_core_kernels/kernels')
    all_files = read_txt('tensorflow')
    for item in all_files:
        if os.path.basename(item) == filename:
            return item
            
def parse_shell(data):
    logging = []
    encoding = 'utf-8'
    if not isinstance(data, str):
        output = data.decode(encoding)
        output = output.split('\n')
    else:
        output = data.split('\n')

    for line in output:
        logging.append(line)

    for line in output:
        if re.findall(r'(core dumped)', line) or re.findall(r'(FAILED|ERROR)', line):
            return True
    return False, logging

class MutatePOSTGRE:
    def __init__(self, project_name, test_files):
        self.killed = 0
        self.alive = 0
        self.project_name = project_name
        self.test_files = test_files
        self.test_files_status = {}

        self.operators = {'REDAWN': False, 'NUMERICAL_PRECISION': False}

        self.REDAWN_COUNTER_alive = 0
        self.REDAWN_COUNTER_killed = 0


    def reset_flag(self):
        self.operators = {'REDAWN': False}

    def determine_operator(self, opt):
        if 'OP_REQUIRE' in opt:
            self.operators['REDAWN'] = True
        if 'numericalPrecision' in opt:
            self.operators['NUMERICAL_PRECISION'] = True
        filtered_operators = [k for k, v in self.operators.items() if v]
        return filtered_operators

    def runProcess(self, exe):
        p = subprocess.Popen(exe, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while(True):
            retcode = p.poll()
            line = p.stdout.readline()
            yield line
            if retcode is not None:
                break

    def pre_run_test_files(self):
        run('./scripts/compiletf.sh', shell=True)
        run('./scripts/build_pip.sh', shell=True)
        run('./scripts/pip_install_.sh', shell=True)

        out_file_name = 'tensorflow_kernel_test_all_run'
        with Pool(10) as p:
            p.map(process_prerun, self.test_files)

    def callback(self, e):
        print('I am in callback!')
        self.event.wait()
        #self.p.terminate()

        if e is not None:
            self.test_files_status[e[0]] = e[1]
        

    def reformat_corrupted_file(self, file_addr):
        #reformat_regex = r'.*\.\(cpp\|hpp\|cu\|c\|cc\|h\)'
        #reformat_command = 'find ' +file_addr+ ' -regex ' +reformat_regex+ ' -exec clang-format -style=file -i {} \;'
        call(['clang-format -i '+ file_addr], shell=True)

    def apply_numerical_precision(self, filtered_operators, original_data_dict, item, operator):
            temp_data_dict = original_data_dict.copy()

            if not os.path.exists('./logging/'+item[5]):
                os.makedirs('./logging/'+item[5])

            flag = False

            if re.findall(r'\bint64\b', temp_data_dict[item[1]]):
                temp_data_dict[item[1]] = re.sub(r'\bint64\b', 'int', temp_data_dict[item[1]])
                flag = True
            if re.findall(r'\buint32_t\b', temp_data_dict[item[1]]):
                temp_data_dict[item[1]] = re.sub(r'\buint32_t\b', 'int32_t', temp_data_dict[item[1]])
                flag = True

            if re.findall(r'\bint64_t\b', temp_data_dict[item[1]]):
                temp_data_dict[item[1]] = re.sub(r'\bint64_t\b', 'int32_t', temp_data_dict[item[1]])
                flag = True

            if re.findall(r'\bsize_t\b', temp_data_dict[item[1]]):
                temp_data_dict[item[1]] = re.sub(r'\bsize_t\b', 'int', temp_data_dict[item[1]])
                flag = True
            
            if item[4] != 'mutated' and flag:
                write_to_disc(temp_data_dict, item[7])    

            self.src = search_for_file(os.path.basename(item[7]))

            #run('./scripts/compiletf.sh', shell=True)
            run('./scripts/build_pip.sh', shell=True)
            run('./scripts/pip_install_.sh', shell=True)
            # target_test = filter_test_files(self.test_files, item[7])
            self.p = multiprocessing.Pool(10) 
            m = multiprocessing.Manager()
            self.item = item
            self.event = m.Event()
            #for i,f in enumerate(self.test_files):
            status = self.p.apply(process, (self.test_files, item[5],))

            test_data = pd.read_csv('test_status.csv')
            if any(elem == True for elem in test_data.iloc[:, 1]):  
                self.REDAWN_COUNTER_killed += 1
                db_obj.updateMstatus(self.item[0], 'killed')
                db_obj.updateMutatedLine(item[0], 'mutated')
            else:
                self.REDAWN_COUNTER_alive += 1
                db_obj.update(self.item[0], 1)
                db_obj.updateMstatus(self.item[0], 'alive')
                db_obj.updateMutatedLine(item[0], 'mutated')
                            # write_to_disc(original_data_dict, item[7])
            target = os.path.dirname(os.path.abspath(self.item[7]))
                #os.remove(self.item[7])
                #cmd = 'cp ' + self.src + ' ' + target
            print('Deleting existing project!')
            cmd1 = 'rm -rf /media/nimashiri/SSD/tensorflow'
            subprocess.call(cmd1, shell=True)
            print('Copying source files to directory for mutation!')
            cmd2 = 'echo "nima1370" | sudo cp -r /home/nimashiri/tensorflow /media/nimashiri/SSD/tensorflow' 
            subprocess.call(cmd2, shell=True)
            subprocess.call('cp -r test_status.csv ./logging/'+item[5])
            subprocess.call('rm -rf test_status.csv', shell=True)
            

    def apply_REDAWN(self, filtered_operators, original_data_dict, item, operator):
            temp_data_dict = original_data_dict.copy()

            if not os.path.exists('./logging/'+item[5]):
                os.makedirs('./logging/'+item[5])
            
            if item[4] != 'mutated':
                for l in range(item[1], item[2]+1):
                    del temp_data_dict[l]
                write_to_disc(temp_data_dict, item[7])
                # self.reformat_corrupted_file(item[7])            

            self.src = search_for_file(os.path.basename(item[7]))

            run('./scripts/compiletf.sh', shell=True)
            run('./scripts/build_pip.sh', shell=True)
            run('./scripts/pip_install_.sh', shell=True)
            # target_test = filter_test_files(self.test_files, item[7])
            self.p = multiprocessing.Pool(10) 
            m = multiprocessing.Manager()
            self.item = item
            self.event = m.Event()
            #for i,f in enumerate(self.test_files):
            status = self.p.apply_async(process, (self.test_files, item[5],))

            test_data = pd.read_csv('test_status.csv')
            if any(elem == True for elem in test_data.iloc[:, 1]):  
                self.REDAWN_COUNTER_killed += 1
                db_obj.updateMstatus(self.item[0], 'killed')
                db_obj.updateMutatedLine(item[0], 'mutated')
            else:
                self.REDAWN_COUNTER_alive += 1
                db_obj.update(self.item[0], 1)
                db_obj.updateMstatus(self.item[0], 'alive')
                db_obj.updateMutatedLine(item[0], 'mutated')
                            # write_to_disc(original_data_dict, item[7])
            target = os.path.dirname(os.path.abspath(self.item[7]))
                #os.remove(self.item[7])
                #cmd = 'cp ' + self.src + ' ' + target
            # print('Deleting existing project!')
            # cmd1 = 'rm -rf /media/nimashiri/SSD/tensorflow'
            # subprocess.call(cmd1, shell=True)
            # print('Copying source files to directory for mutation!')
            # cmd2 = 'echo "nima1370" | sudo cp -r /home/nimashiri/tensorflow /media/nimashiri/SSD/tensorflow' 
            # subprocess.call(cmd2, shell=True)
            # subprocess.call('cp -r test_status.csv ./logging/'+item[5])
            # subprocess.call('rm -rf test_status.csv', shell=True)
                 

    def apply_mutate(self, filtered_operators, temp_data_dict, item, operator):
        for mkind in filtered_operators:
            if mkind == 'REDAWN':
                self.apply_REDAWN(filtered_operators,
                                  temp_data_dict, item, operator)
            # if mkind == 'NUMERICAL_PRECISION':
            #     self.apply_numerical_precision(filtered_operators, temp_data_dict, item, operator)

def main():

    project_name = 'tensorflow_kernel_test'

    #pre run test files to excluding failed ones
    if not os.path.isfile('tensorflow_kernel_test_all_run_files.txt'):
        _files = read_txt(project_name)

        mpost = MutatePOSTGRE(project_name, _files)

        mpost.pre_run_test_files()


    _files = read_txt(valid_tests)

    mpost = MutatePOSTGRE(project_name, _files)

    ds_list = db_obj.filter_table()
    #ds_list = random.sample(ds_list, len(ds_list))
    db_obj.delete_null()

    for item in ds_list:
        # item = ds_list[i]
        # item = list(item)
        if os.path.isfile(item[7]):
            data_dict = read_code_file(item[7])
            print('I am mutating {}'.format(item[7]))
            filtered_operators = mpost.determine_operator(item[6])
            start_time = time.monotonic()
            mpost.apply_mutate(filtered_operators, data_dict, item, filtered_operators[0])
            end_time = time.monotonic()
            print('Duration of mutation on this file: {}'.format(end_time - start_time))
            mpost.reset_flag()


if __name__ == '__main__':
    main()
