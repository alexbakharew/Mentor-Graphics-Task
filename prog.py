import sys
import os
import string
def MoveUp(): # raising into parent dir
    os.chdir("./..")

def MoveDown(path): # descending into dir
    os.chdir("./" + str(path))

def GetValidPath(raw_path, depth=2):
    raw_path = str(raw_path)
    p = raw_path.split("/")
    valid_path = str()
    for i in range(depth, 0, -1):
        valid_path += str(p[len(p) - i]) + "/"
    return valid_path  

def FoldersExisting():#1
    #Checking if both folders are present
    return os.path.isdir("./ft_reference"), os.path.isdir("./ft_run")

def RefRunFiles():
    ref_files = set()
    run_files = set()
    os.chdir("./ft_reference")
    dirs = os.listdir()
    for d in dirs:#1 2 3 ... n
        os.chdir("./" + d)
        files = os.listdir() # *.stdout
        for f in files: # if there are few stdout files
            ref_files.add(GetValidPath(os.getcwd(), 1) + f)
            #append(GetValidPath(os.getcwd(), 1) + f)
        os.chdir("./..")
    os.chdir("./..")
    dirs.clear()
    #----------------------------------------------
    os.chdir("./ft_run")
    dirs = os.listdir()
    for d in dirs:#1 2 3 ... n
        os.chdir("./" + d)
        files = os.listdir() # *.stdout
        for f in files: # if there are few stdout files
            run_files.add(GetValidPath(os.getcwd(), 1) + f)
        os.chdir("./..")
    os.chdir("./..")

    unique_ref_files = ref_files - (ref_files & run_files)
    unique_run_files = run_files - (ref_files & run_files)
    res = list()
    if len(unique_ref_files) > 0 or len(unique_run_files) > 0:
        for f in unique_ref_files:
            res.append("In ft_run there are missing files present in ft_reference:" + GetValidPath(os.getcwd(), 0) + f)
            # print("In ft_run there are missing files present in ft_reference:" , GetValidPath(os.getcwd(), 0) + f)
        
        for f in unique_run_files:
            res.append("In ft_run there are extra files files not present in ft_reference:" + GetValidPath(os.getcwd(), 0) + f)
        
    return res


def ErrorsFinishes():#3
    #checking absence of errors and presence of finishes
    res = []
    os.chdir("./ft_run")
    subdirs = os.listdir()
    for sd in subdirs: # 1, 2, 3, ... n
        os.chdir("./" + str(sd))
        files = os.listdir() 
        for name in files: # *.stdout
            # print("FILE = ", name)
            f = open(name, "r")
            l = 1 #count of lines
            is_finish = False
            for line in f:
                lower_line = line.lower()
                if lower_line.find("error") != -1: # we find error
                    line = line[0:len(line) - 1] # getting rid of \n in the end of line
                    res.append(GetValidPath(os.getcwd(), 1) + name + "(" + str(l) + "): " + line)
                
                if lower_line.find("solver finished at") != -1: #we find finish
                    is_finish = True
                    
                l += 1
        if not is_finish: # we do not find finish
            res.append(GetValidPath(os.getcwd(), 1)  + name + ": missing 'Solver finished at'")
        os.chdir("./..")
    os.chdir("./..") 
    return res


def main():
    folder_count = 0
    os.chdir("./logs")# moving to working directory
    main_dirs = os.listdir()#getting list of main dirictories

    for md in main_dirs:
        os.chdir("./" + str(md))
        test_dirs = os.listdir()# list of test dirs
        for td in test_dirs:
            os.chdir("./" + str(td))
            folder_count += 1
            # print(os.getcwd())
            #five checks
            '''1'''
            ref, run = FoldersExisting()
            if not ref or not run:
                if ref == False:
                    print("FAIL: " + GetValidPath(os.getcwd()))
                    print("directory missing: ft_reference")
                elif run == False:
                    print("FAIL: " + GetValidPath(os.getcwd()))
                    print("directory missing: ft_run")
                os.chdir("./..")
                continue
            '''2'''
            res = RefRunFiles()
            if len(res) == 0:
                print("OK: " + GetValidPath(os.getcwd()))
            else:
                print("FAIL: " + GetValidPath(os.getcwd()))
                for r in res:
                    print(r)
                os.chdir("./..")
                continue

            '''3'''
            res = ErrorsFinishes()
            if len(res) == 0:
                print("OK: " + GetValidPath(os.getcwd()))
            else:
                print("FAIL: " + GetValidPath(os.getcwd()))
                for r in res:
                    print(r)
            os.chdir("./..")    
        os.chdir("./..")
    # print("folder_count=", folder_count)
if __name__ == "__main__":
    main()