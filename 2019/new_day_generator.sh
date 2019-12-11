#!/bin/bash

set -eu

# What about $1?

newDay="$2"
echo "Generating day $newDay"

mkdir "$newDay"
cp template/day.py "$newDay/$newDay.py"
cp template/__init__.py template/question.txt "$newDay"/
