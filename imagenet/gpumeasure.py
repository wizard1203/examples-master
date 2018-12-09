import os
import pandas as pd
import argparse
import operator
import random
import re

def gpumeasure():
    txtdir = 'measurepipeline/'
    pattern = re.compile(r'(?=gpu_speed\s:\[)\d+\.?\d*')
    pattern2 = re.compile(r'gpu_speed')
    pattern3 = re.compile(r'\s:\[')
    file_list = os.listdir(txtdir)
    length = len(file_list)

    outfile = 'gpumeasure.txt'
    out = open(outfile, 'a')
    for i, file in enumerate(file_list):
        lines = open(os.path.join(txtdir, file), 'r')
        speedsum = 0
        j = 0
        for _, line in enumerate(lines):
            # print(line)
            speedstr = pattern.match(line)
            match2 = pattern2.match(line)
            match3 = pattern3.match(line)
            print(speedstr)
            print(match2)
            print(match3)
            if speedstr:
                j += 1
                if j > 50 and j < 151:
                    speedsum += float(speedstr)
        speedave = speedsum / 100
        out.writelines(str(speedave) + file + '\r')
        

if __name__ == '__main__':
    # args = parser.parse_args()
    gpumeasure()
