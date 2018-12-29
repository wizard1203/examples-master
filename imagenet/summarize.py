import os
import pandas as pd
import argparse
import operator
import math
import re
# ------- python gettxt.py -p C:\\Users\\zhtang\\Desktop\\temp\\gpumeasure

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", help="increase output verbosity")
#parser.add_argument('-l', "--label", type=int, help="the num of labels")
#parser.add_argument("-f", "--files", nargs='+', type=str, help="list of files")
parser.add_argument("-p", "--path", default='C:\\Users\\zhtang\\Desktop\\temp\\gpumeasure', type=str, help="path of files")

patnet = re.compile(r'(?:alexnet|resnet50)')
patgpu1 = re.compile(r'(?<=resnet50)[0-9a-zA-Z\(\)\s-]+(?=b)')
patgpu2 = re.compile(r'(?<=alexnet)[0-9a-zA-Z\(\)\s-]+(?=b)')
patbatch = re.compile(r'(?<=b).*(?=n[0-9])')
patworkers = re.compile(r'(?<=[0-9]n).*(?=\.log)')
patspeed = re.compile(r'(?<=gpu_speed=)\d+\.?\d*')
patiotime = re.compile(r'(?<=io_time=)\d+\.?\d*')

batchs = ['8', '16', '32', '64', '128', '256', '512']
workers = ['1', '2', '4', '8', '16', '32', '64']

def getnet(line):
    net = patnet.search(line)
    return net.group()

def getgpu(line):
    if not patgpu1.search(line):
        gpu = patgpu2.search(line)
    else:
        gpu = patgpu1.search(line)
    return gpu.group()

def getbatch(line):
    batch = patbatch.search(line)
    return batch.group()
    
def getworkers(line):
    workers = patworkers.search(line)
    return workers.group()

def getspeed(line):
    speed = patspeed.search(line)
    return speed.group()

# def getbnname(b, n):
#     return 'b' + b + 'n' + n


def summarize(args):
    
    
    savepath = os.path.join(args.path, 'summarize.csv')
    gpus = {}
    
    file_list = os.listdir(args.path)
    for file_name in file_list:
        file_path = os.path.join(args.path, file_name)
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if getgpu(lines[0]) not in gpus:
                gpus[getgpu(lines[0])] = {}
            if getnet(lines[0]) not in gpus[getgpu(lines[0])]:
                gpus[getgpu(lines[0])][getnet(lines[0])] = {}
                
            for b in batchs:
                gpus[getgpu(lines[0])][getnet(lines[0])][b] = {}
                for n in workers:
                    gpus[getgpu(lines[0])][getnet(lines[0])][b][n] = 0.0
            for line in lines:
                gpus[getgpu(lines[0])][getnet(lines[0])][getbatch(line)][getworkers(line)] = getspeed(line)
    
    gpuframes = []
    gpunames = []
    for gpuname, gpu in gpus.items():
        netframes = []
        netnames = []
        for netname, net in gpu.items():
            data = {}
            for batchname, batch in net.items():
                data[batchname] = [bbb for bbb in batch.values()]
            frame = pd.DataFrame(data, index=workers)
            netframes.append(frame)
            netnames.append(netname)
        gpuframe = pd.concat(netframes, keys=netnames, axis=1, join='outer').fillna(0)
        gpuframes.append(gpuframe)
        gpunames.append(gpuname)
        
    summarframe = pd.concat(gpuframes, keys=gpunames, axis=0, join='outer').fillna(0)
    savepath = os.path.join(args.path, 'summarize.csv')
    summarframe.to_csv(savepath, index=True)

if __name__ == '__main__':
    args = parser.parse_args()
    summarize(args)



