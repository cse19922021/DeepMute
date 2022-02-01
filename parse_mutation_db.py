
from util.DBadaptor import DBHandler
from util.fileUtil import csv_writer
import csv

def parse():
    db_obj = DBHandler()

    ds_list = db_obj.filter_table()
    db_obj.delete_null()

    a = []
    for item in ds_list:
        if item[4] == 'mutated':
            a.append(list(item))
    with open("mutation_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(a)

if __name__  == '__main__':
    parse()