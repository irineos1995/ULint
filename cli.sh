#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -t parameterT -l parameterL -r parameterR -c parameterC -d parameterD"
   echo -e "\t-t Training directory for ULint"
   echo -e "\t-l Page to be linter with ULint"
   echo -e "\t-r rules.json file to be loaded to ULint"
   echo -e "\t-c Depth cap of relations"
   echo -d "\t-d .html file to save the documentation of ULint in"
   exit 1 # Exit script after printing help
}

while getopts "t:l:r:c:d:" opt
do
   case "$opt" in
      t ) parameterT="$OPTARG" ;;
      l ) parameterL="$OPTARG" ;;
      r ) parameterR="$OPTARG" ;;
      c ) parameterC="$OPTARG" ;;
      d ) parameterD="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$parameterT" ] && [ -z "$parameterL" ] && [ -z "$parameterR" ] && [ -z "$parameterC" ]
then
   echo "All of the parameters are empty";
   helpFunction
fi

if [ -z "$parameterL" ]
then
    parameterL="None";
fi

if [ -z "$parameterC" ]
then
    parameterC=0;
fi

if [ -z "$parameterT" ] && [ -z "$parameterR" ]
then
    echo "You need either a training directory or a ULint rules.json file";
    exit 1
fi

if [ -z "$parameterT" ]
then
    parameterT="None";
fi

if [ -z "$parameterR" ]
then
    parameterR="None";
fi

if [ -z "$parameterD" ]
then
    parameterD="None";
fi

# Load the virtual environment to load all the dependencies
source venv/bin/activate

python cli.py -t $parameterT -r $parameterR -l $parameterL -c $parameterC -d $parameterD
