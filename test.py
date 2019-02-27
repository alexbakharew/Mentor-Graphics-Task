import sys
import os
import glob
import string
os.chdir("./logs")
main_dir = os.listdir()
for md in main_dir:
    os.chdir("./" + md)
    test_dir = os.listdir()
    for td in test_dir:        
        os.chdir("./" + td)
        report = open("report_test.txt", "w+")
        report.write("JOpa")
        report.close()
        exit(0)
        # ref = open()
        os.chdir("./..")    
    os.chdir("./..")
# print(validPath) 
#dirList = os.listdir()
# for d in dirList:
#     os.chdir("./" + str(d))
#     print(os.listdir())
#     print("\n\n ---------------------------- \n\n")
#     os.chdir("./..")
    