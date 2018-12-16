#!~/miniconda3/envs/py36/bin python
#!/bin/bash
while getopts 'h:' OPT; do
    case $OPT in
        h)
            host="$OPTARG";;
        ?)
            echo "Usage: `basename $0` [options] filename"
    esac
done
shift $(($OPTIND - 1))
echo $host
case $host in
    gpuhome)
        txt = "/home/datasets/imagenet/imagenet_hdf5" ;;
    host143)
        txt = "/home/hpcl/data/imagenet/imagenet_hdf5" ;;
    host145)
        txt = "/media/disk2/data2/imagenet/imagenet_hdf5" ;;
esac
batch_sizes=(16 32 64 128 256)
num_workers=(1 2 4 8 16 32 64)

inti=0
while(( $inti<${#batch_sizes[*]} ))
do
    intj=0
    while(( $intj<${#num_workers[*]} ))
    do
        python main.py -a alexnet --customize --measure alexme1 -b ${batch_sizes[$inti]} -j ${#num_workers[$intj]} --gpu 0 --lr 0.05 --weight-decay 0.00001 --epochs 95 --kind 000 $txt
        let "intj++"
    done
    let "inti++"
done


