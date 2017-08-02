import os

def check_file(a_file):
    flag = False
    if a_file.endswith("xls"):
        flag = True
    if a_file.endswith("xlsx"):
        flag = True
    return flag
def read_path():
    path = r"/home/ubuntu/app/dbfiles/"
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and check_file(str(f))]
def remove_file(a_file):
    path = r"/home/ubuntu/app/dbfiles/"
    path = path + a_file
    os.remove(path)

def read_path2():
    path = r"/home/ubuntu/app/data2/"
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) and "_converted.csv" in f]

def remove_file2(a_file):
    path = r"/home/ubuntu/app/data2/"
    path = path + a_file
    os.remove(path)
#files = read_path2()

#for a_file in files:
#    print a_file
#    print str(a_file).split(".")[0].replace("_converted","")
