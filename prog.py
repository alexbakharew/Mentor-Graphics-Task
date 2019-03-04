# !/usr/bin/python
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

def FoldersExisting(): #1
    #Checking if both folders are present
    return os.path.isdir("./ft_reference"), os.path.isdir("./ft_run")

def RefRunFiles(): #2
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

def RefRunResults(): #4
    ref_stdout = open("./ft_reference/1/1.stdout")
    run_stdout = open("./ft_run/1/1.stdout")
    
    ref_values = []
    max_value = float()
    
    ref_mesh_total = int()
    run_mesh_total = int()

    for line in ref_stdout: # ref file
        if line.find("Memory Working Set Current") > -1:
            val = str()
            for i in range(65, len(line)): #65 - start position of peak memory value in log files  
                if line[i] == " ":
                    break
                val += line[i]
            ref_values.append(float(val))
        elif line.find("MESH::Bricks") > -1:
            val = str()
            for i in range(20, len(line)): # 20 - start position of total value
                if line[i] == " ":
                    break
                val += line[i]
            ref_mesh_total = int(val)


    
    for line in run_stdout:
        if line.find("Memory Working Set Current") > -1:
            val = str()
            for i in range(65, len(line)): #65 - start position of peak memory value in log files  
                if line[i] == "M":
                    break
                val += line[i]
            val = float(val)
            max_value = val if max_value < val else max_value

        elif line.find("MESH::Bricks") > -1:
            val = str()
            for i in range(20, len(line)): # 20 - start position of total value
                if line[i] == " ":
                    break
                val += line[i]
            run_mesh_total = int(val)
    
    # print(ref_mesh_total, " ", run_mesh_total)
    res = []
    for n in ref_values:
        if max_value / n > 4:
            res.append(GetValidPath(os.getcwd(), 2) + ": different 'Memory Working Set Peak' (ft_run={}, ft_reference={}, rel.diff={:.2f}, criterion=4)\n".format(max_value, n, max_value / n))
    df = float(run_mesh_total / ref_mesh_total - 1)
    if df > 0.1:
        res.append(GetValidPath(os.getcwd(), 2) + " different 'Total' of bricks (ft_run={}, ft_reference={}, rel.diff={:.2f}, criterion=0.1)\n".format(run_mesh_total, ref_mesh_total, df))
    return res                        


    # print(ref_values)
    # print(run_values)


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
    result = open("result.txt", "w")#result file for all tests
    os.chdir("./logs")# moving to working directory
    main_dirs = os.listdir()#getting list of main dirictories

    for md in main_dirs:
        os.chdir("./" + str(md))
        test_dirs = os.listdir()# list of test dirs
        for td in test_dirs:
            os.chdir("./" + str(td))
            
            try:
                # myfile = open("myfile.csv", "r+") # or "a+", whatever you need
                # os.open()
                report = os.open("report.txt", os.O_WRONLY | os.O_CREAT )# report file for current test
            except IOError:
                print("Could not open file! Please close file!")
                exit(0)
            
            '''five checks'''
            '''1'''
            ref, run = FoldersExisting()
            if not ref or not run:
                result.write("FAIL: " + GetValidPath(os.getcwd()) + "\n")
                if ref == False:
                    # print("FAIL: " + GetValidPath(os.getcwd()))
                    os.write(report,"directory missing: ft_reference\n".encode())
                    result.write("directory missing: ft_reference\n")
                    
                elif run == False:
                    # print("FAIL: " + GetValidPath(os.getcwd()))
                    os.write(report, "directory missing: ft_run\n".encode())
                    result.write("directory missing: ft_run\n")
                    
                os.chdir("./..") # End of check for this test
                os.close(report) # close report file for current test
                continue
            '''2'''
            res = RefRunFiles()
            if not (len(res) == 0):                
                result.write("FAIL: " + GetValidPath(os.getcwd()) + "\n")
                for r in res:
                    os.write(report, (r + "\n").encode())                    
                    result.write(r + "\n")

                os.chdir("./..") # End of check for this test
                os.close(report) # close report file for current test
                continue
            '''3'''
            fail = False
            res = ErrorsFinishes()
            if not(len(res) == 0):
                result.write("FAIL: " + GetValidPath(os.getcwd()) + "\n")
                for r in res:
                    os.write(report, (r + "\n").encode())
                    result.write(r + "\n")
                fail = True
            '''4'''
            res = RefRunResults()
            if not(len(res) == 0):
                result.write("FAIL: " + GetValidPath(os.getcwd()) + "\n")
                for r in res:
                    os.write(report, r.encode())
                    result.write(r)
                fail = True

            '''end of checks'''
            if not fail:
                result.write("OK: " + GetValidPath(os.getcwd(), 2) + "\n")

            os.chdir("./..")  
            os.close(report)
        os.chdir("./..")
    result.close()


if __name__ == "__main__":
    main()