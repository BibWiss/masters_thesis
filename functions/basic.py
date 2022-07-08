# -----------------------------------
# BASIC HELPFUL FUNCTIONS
# -----------------------------------

import os
import pandas as pd

# -----------------------------------
# READING/WRITING FILES
# -----------------------------------

# READ_FILE()
# -----------------------------------
# FILEPATH = str(); name of the file/filepath
# TEXT/DF = file content

# read files differently depending on their extension
def read_file(filepath):
    if filepath[-4:] == ".pkl":
        df = pd.read_pickle(filepath)
        return df
    elif filepath[-4:] == ".txt":
        with open(filepath, "r", encoding="utf-8") as textfile:
            text = textfile.read()
        return text


# -----------------------------------
# CREATING DIRECTORIES
# -----------------------------------

# GET_CURRENT_DIR()
# -----------------------------------
# NO INPUT
# CURRENT_DIR = str(); actual working path

def get_current_dir():
    current_dir = os.getcwd()
    return current_dir

# CREATE_DIR()
# -----------------------------------
# DIRNAME = str(); name of the directory to create

def create_dir(dirName):
    current_dir = get_current_dir()
    dir_to_create = current_dir + "\\" + dirName
    try:
        os.makedirs(dir_to_create)
        print("Directory " , dir_to_create ,  " created.") 
    except FileExistsError:
        print("Directory " , dir_to_create ,  " already exists, save data there.") 