#!/bin/bash

if (( $# != 2 )); then 
    echo "Usage: $0 <dir> <ofile>";
    exit;
fi

ffmpeg -pattern_type glob -i $1'*.png' $2

rm $1/*