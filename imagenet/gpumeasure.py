import os
import pandas as pd
import argparse
import operator
import random
import re

def gpumeasure():
    txtdir = 'measurepipeline/'
    pattern = re.compile(r'(?<=gpu_speed\s:\[)\d+\.?\d*')
    
    file_list = os.listdir(txtdir)
    length = len(file_list)

    outfile = os.path.join(txtdir, 'gpumeasure.txt')
    out = open(outfile, 'a')
    for i, file in enumerate(file_list):
        lines = open(os.path.join(txtdir, file), 'r')
        speedsum = 0
        for i, line in enumerate(lines):
            speed = float(pattern.findall(line))
            if i > 50 and i < 151:
                speedsum += speed
        speedave = speedsum / 100
        out.writelines(str(speedave), file_list)
        

if __name__ == '__main__':
    # args = parser.parse_args()
    gpumeasure()
