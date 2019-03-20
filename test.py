import sys
import os
import glob
import string
import re
def main():
    # os.chdir("./logs/14-HEAT_TRANSFER_IN_SOLID/00003-_ss_ss__ins-Tfixed/ft_run/1")
    file = open("./logs/14-HEAT_TRANSFER_IN_SOLID/00003-_ss_ss__ins-Tfixed/ft_reference/1/1.stdout")
    result = []
    for line in file:
        m = re.search("MESH::Bricks: Total=([0-9]+.*[0-9]*) Gas=([0-9]+.*[0-9]*) Solid=([0-9]+.*[0-9]*) Partial=([0-9]+.*[0-9]*) Irregular=([0-9]+.*[0-9]*)", line)
        if m != None:
            print(m.group(0))
            print(m.group(1))
        #     print(m.group(2))

            
#     values = []
#     for r in result:
#         tmp = re.findall("\d*[.]\d*", str(r))
#         values.append(tmp)
    
#     print(values)


if __name__ == "__main__":
    main()
    