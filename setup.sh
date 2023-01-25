#!/bin/bash
################################################################################
# oscar
##
# Purpose:
## 
################################################################################
#________________
#|_File_History_|_______________________________________________________________
#|_Programmer______|_Date_______|_Comments______________________________________
#| Max Marshall    | 2023-01-24 | Created File
#|
#|
#|

if [[ ! -d ".venv" ]]; then
	python3 -m venv .venv
	echo "created .venv"
else
	echo ".venv already exists"
fi

source .venv/bin/activate

pip3 install -r requirements.txt
