# !/usr/bin/python
import sys
import os
import string
import re
def FoldersExisting(path, report): #1
    #Checking if both folders are present
    ref_result = os.path.isdir(path + "/ft_reference")
    run_result = os.path.isdir(path + "/ft_run")
    result = ""

    if not ref_result:
        result = "ft_reference"

    if not run_result:
        result = "ft_run"

    if len(result) > 0:# absence of folder
        report.write("directory missing: {}\n".format(result))
        return False

    return True

def RefRunFiles(path, report): #2

    def GetFiles(path, folder, file_set):# This function is collecting names of stdout files, which exist in current folder, into file set
        dirs = os.listdir(path + "/" + folder)
        for d in dirs:#1 2 3 ...
            files = os.listdir(path + "/" + folder + "/" + d)
            for f in files:
                file_set.add(d + "/" + f)

    ref_files = set() # set of unique *.stdout files in ref folder
    run_files = set() # set of unique *.stdout files in run folder

    GetFiles(path, "ft_reference", ref_files)
    GetFiles(path, "ft_run", run_files)

    unique_ref_files = ref_files - (ref_files & run_files)
    unique_run_files = run_files - (ref_files & run_files)
    # trick with sets from descrete math - symmetric difference
    # now we have files, which is unique for each folder

    if len(unique_ref_files) > 0 or len(unique_run_files) > 0:
        for f in unique_ref_files:
            report.write("In ft_run there are missing files present in ft_reference: '{}'\n".format(f))

        for f in unique_run_files:
            report.write("In ft_run there are extra files files not present in ft_reference: '{}'\n".format(f)) 
        return False
    else:
        return True

def ProcessFiles(path, report): #3, #4
    
    def GetFileList(path, folder): # this function is collecting Files of current folder and return list of them
        file_list = []
        dirs = os.listdir(path + "/" + folder)
        for d in dirs:#1 2 3 ...
            files = os.listdir(path + "/" + folder + "/" + d)
            for f in files:
                file_list.append(d + "/" + f)
        return file_list
        
    def ReadFile(file, track, report): # Read file. Find all errors, finishes(yes or no). Function will return max peak value and last mesh value in curent test
        # track is a path to the file(e.g. 1/1.stdout)
        is_finish = False # 
        peak_val = -1.0 # initial value
        mesh_val = -1.0 # initial value
        line_count = 0
        for line in file:

            line_count += 1
            lower_line = line.lower()

            res = re.search("error", lower_line)
            if res != None:
                func_result = False
                report.write("{}({}): {}".format(track, line_count, line))
                continue
            
            res = re.search("solver finished at", lower_line)
            if res != None:
                is_finish = True
                continue
            
            res = re.search("Peak = \d+.\d+ Mb", line)
            if res != None:
                val = float(re.search("\d+[.]\d+", str(res)).group(0))
                if val > peak_val:
                    peak_val = val
                continue
            
            res = re.search("MESH::Bricks: Total=\d+.", line)
            if res != None:
                mesh_val = int(re.search("\d+[ ]", str(res)).group(0))
                continue  
                
        if not is_finish:
            report.write("{}: missing 'Solver finished at'".format(track))
        
        return peak_val, mesh_val


    file_list = GetFileList(path, "ft_run")   # As we checked that all folders have the same set of files,
                                        # we can launch GetFileList("ft_reference") with same result.
                                        # We just get set of files, which we need to check
    for track in file_list: # track is a sinonym to the path

        ref_stdout = open(path + "/ft_reference/" + track)
        run_stdout = open(path + "/ft_run/" + track)

        run_peak_val, run_mesh_val = ReadFile(run_stdout, track, report)
        ref_peak_val, ref_mesh_val = ReadFile(ref_stdout, track, report)

        if run_peak_val / ref_peak_val > 4:
            report.write("{}: different 'Memory Working Set Peak' (ft_run={}, ft_reference={}, rel.diff={:.2f}, criterion=4)\n".format(track, run_peak_val, ref_peak_val, run_peak_val / ref_peak_val))

        df = float(run_mesh_val / ref_mesh_val - 1)
        if df > 0.1:
            report.write("{}: different 'Total' of bricks (ft_run={}, ft_reference={}, rel.diff={:.2f}, criterion=0.1)\n".format(track, run_mesh_val, ref_mesh_val, df))

def PrintReport(path): # function for printing report of current test
    report = open(path + "/report.txt", "r")
    if os.stat(path + "/report.txt").st_size == 0:
        print("OK: " + path)
    else:
        print("FAIL: " + path)
        for line in report:
            print(line.rstrip())
    report.close()

def CheckTest(path): # We will launch all 4 checks consistently
    report = open(path + "/report.txt", "w")

    if not FoldersExisting(path, report): #1
        report.close()
        return
    
    if not RefRunFiles(path, report): #2
        report.close()        
        return
    ProcessFiles(path, report)
    report.close()
    

def main():
    os.chdir("./logs")# move to working directory
    main_dirs = os.listdir()
    main_dirs.sort()
    for md in main_dirs:
        sub_dirs = os.listdir(md)
        sub_dirs.sort()
        for sd in sub_dirs:
            CheckTest(md + "/" + sd + "/")
            PrintReport(md + "/" + sd + "/")

if __name__ == "__main__":
    main()