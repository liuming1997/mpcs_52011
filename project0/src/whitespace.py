"""
MPCS 52011 Project 0
Ming Liu

Whitespace remover
"""

#!/usr/bin/env python

# we use regex here to make finding and removing things easier
import re
import argparse
import os.path

def whitespace(path):
    """
    Take a path to a file and remove all of the whitespace and comments.
    """
    try:
        # read file
        with open(path, 'r') as f:
            thing = f.read()
        
        # regex black magic
        pattern = re.compile("^\s+|\ |(//.+)|(/*(.|\n)+\*/)|^$\s*", re.MULTILINE)
        export = re.sub(pattern, "", thing)
        # removes the empty newline at the beginning
        export = export.strip()
        
        # build the export path, remove the file itself in the path, and get the file name
        # if statement checks for absolute or relative paths
        if os.path.sep in path:
            exportPath = os.path.split(path)
            fileName = exportPath[-1]
            exportPath = exportPath[:-1]
        else:
            exportPath = ""
            fileName = path

        # change the file extension
        fileName = fileName.replace(".in", ".out")
        
        # we split up exportPath, now bring it together:
        output = ""
        if exportPath != "":
            for i in exportPath:
                output = os.path.join(output, i)
        output = os.path.join(output, fileName)
        
        with open(output, 'w') as o:
            o.write(export)
    
        print("Successfully exported to " + output)

    except:
        print("Error: " + path + " is not a valid file path. Please double-check and try again.")
        
    return None

def main():
    """
    Note: 
    You DO NOT run 'python whitespace.py trim foobar.in'.
    Just 'python whitespace.py foobar.in' works, because you only have one argument.
    In fact, it won't like it if you try the former.
    """
    # invoke argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('trim', help="Remove all comments and whitespace from target file.", type=str)
    args = parser.parse_args()

    if args.trim:
        whitespace(args.trim)

if __name__ == "__main__":
    main()