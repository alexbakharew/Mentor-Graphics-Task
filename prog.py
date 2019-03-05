# !/usr/bin/python
import sys
import os
import string
def MoveUp(): # raising into parent dir
    os.chdir("./..")

def MoveDown(path): # descending into dir
    os.chdir("./" + str(path))

def GetValidPath(raw_path, depth=2): #function for getting path of neccessary depth
    raw_path = str(raw_path)
    p = raw_path.split("/")
    valid_path = str()
    for i in range(depth, 0, -1):
        valid_path += str(p[len(p) - i]) + "/"
    return valid_path  

def FoldersExisting(): #1
    #Checking if both folders are present
    return os.path.isdir("./ft_reference"), os.path.isdir("./ft_run")

def RefRunFiles(): #2
    ref_files = set() # set of unique *.stdout files in ref folder
    run_files = set() # set of unique *.stdout files in run folder
    MoveDown("./ft_reference")
    dirs = os.listdir()
    for d in dirs:#1 2 3 ... n
        MoveDown("./" + d)
        files = os.listdir() # *.stdout
        for f in files: # if there are few stdout files
            ref_files.add(GetValidPath(os.getcwd(), 1) + f)
        MoveUp()
    MoveUp()
    dirs.clear()
    #----------------------------------------------
    MoveDown("./ft_run")
    dirs = os.listdir()
    for d in dirs:#1 2 3 ... n
        MoveDown("./" + d)
        files = os.listdir() # *.stdout
        for f in files: # if there are few stdout files
            run_files.add(GetValidPath(os.getcwd(), 1) + f)
        MoveUp()
    MoveUp()

    unique_ref_files = ref_files - (ref_files & run_files)
    unique_run_files = run_files - (ref_files & run_files)
    # trick with sets from descrete math - symmetric difference
    # now we have files, which is unique for each folder
    res = list()
    if len(unique_ref_files) > 0 or len(unique_run_files) > 0:
        for f in unique_ref_files:
            res.append("In ft_run there are missing files present in ft_reference: '{}{}'\n".format(GetValidPath(os.getcwd(), 0), f))
            
        for f in unique_run_files:
            res.append("In ft_run there are extra files files not present in ft_reference: '{}{}'\n".format(GetValidPath(os.getcwd(), 0), f))
            
    return res

def ErrorsFinishes():#3
    #checking absence of errors and presence of finishes
    res = []
    MoveDown("./ft_run")
    subdirs = os.listdir()
    for sd in subdirs: # 1, 2, 3, ... n
        MoveDown("./" + str(sd))
        files = os.listdir() 
        for name in files: # *.stdout
            f = open(name, "r")
            l = 1 # count of lines
            is_finish = False
            for line in f:
                lower_line = line.lower()
                if lower_line.find("error") != -1: # we find error
                    line = line[0:len(line) - 1] # getting rid of \n in the end of the line
                    res.append(GetValidPath(os.getcwd(), 1) + name + "(" + str(l) + "): " + line + "\n")
                
                if lower_line.find("solver finished at") != -1: #we find finish
                    is_finish = True
                    
                l += 1
        if not is_finish: # we do not find finish
            res.append(GetValidPath(os.getcwd(), 1)  + name + ": missing 'Solver finished at'\n")
        MoveUp()
    MoveUp() 
    return res

def RefRunResults(): #4
    f = str()
    MoveDown("./ft_run")
    files = os.listdir() # getting info about folder name in whole test
    # Sometimes we may have 2/2.stdout files, not only 1/1.stdout
    # So it is improper to use 1/1.stdout everywhere
    if len(files) == 1:
        f = str(files[0])
    else:
        # This case is posible but not mentioned in task, when we have two or more result folders in test
        print("\nFATAL ERROR\n")
        exit(-1)

    MoveUp()
    ref_stdout = open("./ft_reference/{}/{}.stdout".format(f, f))
    run_stdout = open("./ft_run/{}/{}.stdout".format(f, f))
    
    ref_max_value = float()
    run_max_value = float()
    
    ref_mesh_total = int()
    run_mesh_total = int()

    for line in ref_stdout: # working with ref file
        if line.find("Memory Working Set Current") > -1: # Memory set string
            val = str()
            for i in range(65, len(line)): # 65 - start position of peak memory value in log files  
                if line[i] == " ":
                    break
                val += line[i]
            val = float(val)
            ref_max_value = val if val > ref_max_value else ref_max_value
        
        elif line.find("MESH::Bricks") > -1: # mesh string
            val = str()
            for i in range(20, len(line)): # 20 - start position of total value in log file
                if line[i] == " ":
                    break
                val += line[i]
            ref_mesh_total = int(val)

    for line in run_stdout: # working with run file
        if line.find("Memory Working Set Current") > -1: # Memory set string
            val = str()
            for i in range(65, len(line)): # 65 - start position of peak memory value in log files  
                if line[i] == " ":
                    break
                val += line[i]
            val = float(val)
            run_max_value = val if val > run_max_value else run_max_value

        elif line.find("MESH::Bricks") > -1: # mesh string
            val = str()
            for i in range(20, len(line)): # 20 - start position of total value in log file
                if line[i] == " ":
                    break
                val += line[i]
            run_mesh_total = int(val)
    
    res = []
    if run_max_value / ref_max_value > 4:
            res.append("{}/{}.stdout: different 'Memory Working Set Peak' (ft_run={}, ft_reference={}, rel.diff={:.2f}, criterion=4)\n".format(f, f, run_max_value, ref_max_value, run_max_value / ref_max_value))
    df = float(run_mesh_total / ref_mesh_total - 1)
    if df > 0.1:
        res.append("{}/{}.stdout: different 'Total' of bricks (ft_run={}, ft_reference={}, rel.diff={:.2f}, criterion=0.1)\n".format(f, f, run_mesh_total, ref_mesh_total, df))
    return res                        

def main():
    result = os.open("result.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)#result file for all tests
    MoveDown("./logs")# moving to working directory
    main_dirs = os.listdir()#getting list of main dirictories
    main_dirs.sort()
    
    for md in main_dirs:
        MoveDown("./" + str(md))
        test_dirs = os.listdir()# list of test dirs
        test_dirs.sort() # sorting names of dirs
        for td in test_dirs:
            MoveDown("./" + str(td))
            report = os.open("report.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC)# report file for current test
            
            '''five checks'''
            '''1'''
            ref, run = FoldersExisting()
            if not ref or not run:
                os.write(result, ("FAIL: " + GetValidPath(os.getcwd()) + "\n").encode())
                if ref == False:
                    os.write(report,"directory missing: ft_reference\n".encode())
                    os.write(result, "directory missing: ft_reference\n".encode())
                    
                elif run == False:
                    os.write(report, "directory missing: ft_run\n".encode())
                    os.write("directory missing: ft_run\n".encode())
                    
                MoveUp() # End of check for this test
                os.close(report) # close report file for current test
                continue
            '''2'''
            res = RefRunFiles()
            if len(res) != 0:                
                os.write(result, ("FAIL: " + GetValidPath(os.getcwd()) + "\n").encode())
                for r in res:
                    os.write(report, r.encode())                    
                    os.write(result, r.encode())

                MoveUp() # End of check for this test
                os.close(report) # close report file for current test
                continue
            '''3'''
            res = ErrorsFinishes()
            fail = False
            if len(res) != 0:
                os.write(result, ("FAIL: " + GetValidPath(os.getcwd()) + "\n").encode())
                for r in res:
                    os.write(report, r.encode())
                    os.write(result, r.encode())
                fail = True
            '''4'''
            res = RefRunResults()
            if len(res) != 0:
                os.write(result, ("FAIL: " + GetValidPath(os.getcwd()) + "\n").encode())
                for r in res:
                    os.write(report, r.encode())
                    os.write(result, r.encode())
                fail = True

            '''end of checks'''

            if not fail:
                os.write(result, ("OK: " + GetValidPath(os.getcwd(), 2) + "\n").encode())
            MoveUp()  
            os.close(report)
        MoveUp()
    os.close(result)

if __name__ == "__main__":
    main()