#! /bin/bash

IP=/home/rathers/mtbtest/file.tar.gz
OP=/home/rathers/mtbtest/

for i in {1..100}
do
    NEW="${OP}file${i}.tar.gz"
    cp $IP $NEW
done

