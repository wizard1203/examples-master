#!~/miniconda3/envs/py36/bin python
#!/bin/bash

measure(){
    batch_sizes=(16 32 64 128 256 512)
    num_workers=(1 2 4 8 16 32 64)
    domeasure ${#batch_sizes[*]} $(echo ${batch_sizes[*]}) ${#num_workers[*]} $(echo ${num_workers[*]})

}

measurehost145(){
    #batch_sizes=(16 32 64 128)
    #num_workers=(1 2 4 8 16 32 64)
    #domeasure ${#batch_sizes[*]} $(echo ${batch_sizes[*]}) ${#num_workers[*]} $(echo ${num_workers[*]})

    batch_sizes=(256 512)
    num_workers=(4 8 16)
    domeasure ${#batch_sizes[*]} $(echo ${batch_sizes[*]}) ${#num_workers[*]} $(echo ${num_workers[*]})
}

domeasure(){
    local origarray
    local len_batchs
    local len_workers
    local length=$[ $# ]

    origarray=($(echo "$@"))
    len_batchs=${origarray[0]}
    #index_workers=${origarray[`expr $len_batchs + 1`]}
    index_workers=`expr $len_batchs + 1`
    for (( i=1; $i<=$len_batchs; i++ )){
        for (( j=`expr $index_workers + 1`; $j<$length; j++ )){
            python main.py -a alexnet --customize --measure alexme1 -b ${origarray[$i]} -j ${origarray[$j]} --gpu 0 --lr 0.05 --weight-decay 0.00001 --epochs 95 --kind 000 $txt
            echo "i : $i, j: $j"
            echo " batch: ${origarray[$i]}, workers: ${origarray[$j]} "
        }
    }
}

domeasure2(){
    inti=0
    while(( $inti<${#batch_sizes[*]} ))
    do
        intj=0
        while(( $intj<${#num_workers[*]} ))
        do
            python main.py -a resnet50 --measure resme1 -b ${batch_sizes[$inti]} -j ${num_workers[$intj]} --gpu 0 --lr 0.05 --weight-decay 0.00001 --epochs 95 --kind 000 $txt
            echo "i : $inti, j: $intj"
            echo " batch: ${batch_sizes[$inti]}, workers: ${num_workers[$intj]} "
            let "intj++"
        done
        let "inti++"
    done
}

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
        txt="/home/datasets/imagenet/imagenet_hdf5"
        measure
        ;;
    host12)
        txt="/data/03/imagenet/imagenet_hdf5"
        measure
        ;;
    host143)
        txt="/home/hpcl/data/imagenet/imagenet_hdf5"
        measure
        ;;
    host145)
        txt="/media/disk2/data2/imagenet/imagenet_hdf5"
        measurehost145
        ;;
esac



