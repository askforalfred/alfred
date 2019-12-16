#!/bin/bash

# filename
FILENAME=alfred_data.zip

if [ "$1" = "json" ]
then
    echo "Downloading JSONs ..."
    wget --load-cookies /tmp/cookies.txt "https://drive.google.com/a/cs.washington.edu/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://drive.google.com/a/cs.washington.edu/uc?export=download&id=1PzS5XaEcGsYtpOmDAbdL0wdvEB91Gb6T' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1PzS5XaEcGsYtpOmDAbdL0wdvEB91Gb6T" -O $FILENAME && rm -rf /tmp/cookies.txt
elif [ "$1" = "json_feat" ]
then
    echo "Downloading JSONs and Resnet18 feats ..."
    wget --load-cookies /tmp/cookies.txt "https://drive.google.com/a/cs.washington.edu/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://drive.google.com/a/cs.washington.edu/uc?export=download&id=1PBEF5qW_TKLCFYd2Dt7_SQkkgNC9jPFd' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1PBEF5qW_TKLCFYd2Dt7_SQkkgNC9jPFd" -O $FILENAME && rm -rf /tmp/cookies.txt
elif [ "$1" = "json_feat_imgs" ]
then
    echo "Downloading JSONs, Resnet18 feats, and Images ..."
    echo "TODO"
    wget --load-cookies /tmp/cookies.txt "https://drive.google.com/a/cs.washington.edu/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://drive.google.com/a/cs.washington.edu/uc?export=download&id=TODO' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=TODO" -O $FILENAME && rm -rf /tmp/cookies.txt
else
    echo "Failed: Usage download_data.sh json | json_feat | json_feat_imgs"
    exit 1
fi

# remove json folder from repo
REPO_JSON_FOLDER='./json_2.1.0'
if [ -d "$REPO_JSON_FOLDER" ]; then
  # Take action if $DIR exists. #
  echo "Removing json_2.1.0 from repo"
  rm -r $REPO_JSON_FOLDER
fi

# unzip and delete zip
unzip $FILENAME && rm $FILENAME