# Usage Instructions

This is a basic implementation of a cli via a python script that will, given a root folder, upload all files in folder and subfolers to a aws bucket.

## Install

1. Insall the required python packages in the requirments.txt file.
  * Python version is 3.8.
2. You are now ready to run the script.

## Usage

1. Run the cli_interface.py scipt with given arguments.
  * To upload give the __--u__ argument and give a path to the root folder that you want to upload.
    * path can be relative or absolute

  * To download give the __--d__ argument. The script will download all files with structure in tacted to the current directory.

### Side Note
  This is a basic impelmentationa and will not work correctly should a structure be uploaded and then a different structure is uploaded to the current structure


### Todos
  1. progress bar
  2. faster tree traversal
  3. package up as an actuall cli
