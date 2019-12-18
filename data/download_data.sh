#!/bin/bash

# filename
FILENAME=alfred_data.zip

if [ "$1" = "json" ]
then
    echo "Downloading JSONs ..."
    wget https://storage.googleapis.com/alfred_dataset/data/json_2.1.0.zip
elif [ "$1" = "json_feat" ]
then
    echo "Downloading JSONs and Resnet18 feats ..."
    wget https://storage.googleapis.com/alfred_dataset/data/json_feat_2.1.0.zip
elif [ "$1" = "full" ]
then
    echo "Downloading JSONs, Resnet18 feats, Images, Videos, and PDDL states ..."
    wget --load-cookies /tmp/cookies.txt "https://drive.google.com/a/cs.washington.edu/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://drive.google.com/a/cs.washington.edu/uc?export=download&id=1xe_asKo6Kb7nQ3c-agPqnhGT7SDJdn84' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1xe_asKo6Kb7nQ3c-agPqnhGT7SDJdn84" -O $FILENAME && rm -rf /tmp/cookies.txt
else
    echo "Failed: Usage download_data.sh json | json_feat | full"
    exit 1
fi

# unzip and delete zip
unzip $FILENAME && rm $FILENAME