import sys
import os
import glob
import string
import re
def main():
    # os.chdir("./logs/14-HEAT_TRANSFER_IN_SOLID/00003-_ss_ss__ins-Tfixed/ft_run/1")
    file = open("./logs/14-HEAT_TRANSFER_IN_SOLID/00003-_ss_ss__ins-Tfixed/ft_run/1/1.stdout")
    result = []
    # for line in file:
    #     match = re.findall("Current = \d*.\d* Mb.* Peak = \d*.\d* Mb", line)
    #     if len(match) > 0:
    #         result.append(match)
    # values = []
    # for r in result:
    #     tmp = re.findall("\d*[.]\d*", str(r))
    #     values.append(tmp)
    
    # print(values)
    f = open("tmp", )
    for line in f:
        print(line)

if __name__ == "__main__":
    main()
    