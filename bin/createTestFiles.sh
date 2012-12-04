#! /bin/bash

IP=/home/rathers/1k.tar.gz
OP=/home/rathers/tmp/mtbtest/

for i in {1..500}
do
    NEW="${OP}file${i}.tar.gz"
    cp $IP $NEW
done

