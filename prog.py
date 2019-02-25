import sys
import os
import string
def MoveUp(): # raising into parent dir
    os.chdir("./..")

def MoveDown(path): # descending into dir
    os.chdir("./" + str(path))

def GetValidPath(raw_path):
    raw_path = str(raw_path)
    p = raw_path.split("/")
    valid_path = str(p[len(p) - 2]) + "/" + str(p[len(p) - 1])
    return valid_path  

def FoldersExisting():#1
    #Checking if both folders are present
    return os.path.isdir("./ft_reference"), os.path.isdir("./ft_run")

def ErrorsFinishes():#2
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
                    res.append(GetValidPath(os.getcwd() + "(" + str(line) + "): " + line))
                    #print()
                
                if lower_line.find("solver finished at") != -1: #we find finish
                    is_finish = True
                    
                l += 1
        if not is_finish: # we do not find finish
            res.append(GetValidPath(os.getcwd()) + "/" + name + ": missing 'Solver finished at'")
        os.chdir("./..")
    os.chdir("./..") 
    return res


def main():
    os.chdir("./logs")# moving to working directory
    main_dirs = os.listdir()#getting list of main dirictories
    for md in main_dirs:
        os.chdir("./" + str(md))
        test_dirs = os.listdir()# list of test dirs
        for td in test_dirs:
            os.chdir("./" + str(td))
            #five checks
            '''1'''
            ref, run = FoldersExisting()
            if not ref or not run:
                if ref == False:
                    print("FAIL: " + GetValidPath(os.getcwd()))
                    print("directory missing: ft_reference")
                if run == False:
                    print("FAIL: " + GetValidPath(os.getcwd()))
                    print("directory missing: ft_run")
                os.chdir("./..")
                break
            
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

if __name__ == "__main__":
    main()