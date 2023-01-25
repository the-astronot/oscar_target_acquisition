#!/bin/bash
################################################################################
# oscar
##
# Purpose:
## 
################################################################################
"""
________________
|_File_History_|_______________________________________________________________
|_Programmer______|_Date_______|_Comments______________________________________
| Max Marshall    | 2023-01-24 | Created File
|
|
|
"""

# Get file directory
FILE_LOC="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd)"

source $FILE_LOC/../.venv/bin/activate

python3 $FILE_LOC/../src/main.py

deactivate
