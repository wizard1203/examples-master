import os
import pandas as pd
import argparse
import operator
import random
import re
import argparse

parser = argparse.ArgumentParser(description='GPU measure')
parser.add_argument('-t', '--txt', default='measurepipeline', type=str,
                    help='sssss')
parser.add_argument('-o', '--outname', default='gpumeasure', type=str,
                    help='gpumeasure file name')

def gpumeasure(args):
    txtdir = args.txt
    pattern = re.compile(r'(?<=gpu_speed\s:\[)\d+\.?\d*')
    file_list = os.listdir(txtdir)
    length = len(file_list)
    
    outfile = args.outname + '.txt'
    out = open(outfile, 'a')
    for i, file in enumerate(file_list):
        lines = open(os.path.join(txtdir, file), 'r')
        speedsum = 0
        j = 0
        for _, line in enumerate(lines):
            # print(line)
            speedstr = pattern.search(line)
            # print(speedstr)
            if speedstr:
                j += 1
                print(j, speedstr.group())
                if j > 50 and j < 151:
                    speedsum += float(speedstr.group())
                if j == 151:
                    break
        speedave = speedsum / 100
        out.writelines(file + ': *===' + str(speedave) + '\n')
        lines.close()
    out.close()

if __name__ == '__main__':
    args = parser.parse_args()
    gpumeasure(args)
