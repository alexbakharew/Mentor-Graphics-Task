import sys
import os
import string
os.chdir("./logs")
main_dir = os.listdir()
for md in main_dir:
    os.chdir("./" + md)
    test_dir = os.listdir()
    for td in test_dir:        
        os.chdir("./" + td)    
        ref = os.listdir("./ft_reference/")
        run = os.listdir("./ft_run/")
        # os.chdir("./ft_reference")
        for d in ref:
            # print("DEBUGGING: ", os.getcwd())
            os.chdir("./ft_reference" + "/" + d)
            print(os.listdir())
            os.chdir("./../..")
        os.chdir("./..")    
    os.chdir("./..")
# print(validPath) 
#dirList = os.listdir()
# for d in dirList:
#     os.chdir("./" + str(d))
#     print(os.listdir())
#     print("\n\n ---------------------------- \n\n")
#     os.chdir("./..")
    