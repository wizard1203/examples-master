#!~/miniconda3/envs/py36/bin python
#!/bin/bash
while getopts 'host:' OPT; do
    case $OPT in
        d)
            host="$OPTARG";;
        ?)
            echo "Usage: `basename $0` [options] filename"
    esac
done
case host in
    gpuhome)
        txt = "/home/datasets/imagenet/imagenet_hdf5" ;;
    host143)
        txt = "/home/hpcl/data/imagenet/imagenet_hdf5" ;;
    host145)
        txt = "/media/disk2/data2/imagenet/imagenet_hdf5" ;;
esac
shift $(($OPTIND - 1))
batch_sizes=(16 32 64 128 256)
num_workers=(1 2 4 8 16 32 64)
for batch in batch_sizes
do
    for workers in num_workers
    do
        python main.py -a alexnet --customize --measure alexme1 -b $batch -j $workers --gpu 0 --lr 0.05 --weight-decay 0.00001 --epochs 95 --kind 000 $txt
    done
done

