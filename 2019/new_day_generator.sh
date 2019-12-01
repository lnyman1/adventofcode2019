#!/bin/bash

if [ "$1" != "-d" ]; then
  usage;
fi

echo "Generating day$2"

newDay="$2"

mkdir $newDay
cp ./template/day.py ./$newDay/"$newDay.py"
cp ./template/__init__.py ./$newDay/__init__.py
cp ./template/question.txt ./$newDay/question.txt
