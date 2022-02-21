Note:
This file is called 'whitespace.py' but does remove whitespace and comments as well.

How to compile:

Python doesn't really do compiling in the way other languages do it. If you want bytecode, you can run from a terminal with Python (from the directory that whitespace.py is in):
python3 -m py_compile whitespace.py (Unix)
python -m py_compile whitespace.py (Windows Powershell)
or use the provided compile.py file in your development environment (your workspace must be the directory of whitespace.py for it to work, so use the terminal instead).
The bytecode file has the extension .pyc, and is found in a folder labeled "__pycache__" inside src.

py_compile is a standard Python library package and does not need installing.

How to run:

From your command line, with Python installed:
Windows Powershell:
python path\to\whitespace.py path\to\input_file.in (should just default to python3)
Unix terminal:
python3 path/to/whitespace.py path/to/input_file.in (DO NOT use python2; it probably won't work, and has NOT been tested.)

On Unix, the file already has the shebang header to mark it as executable. If you wish to make it so, run the following:
chmod +x path/to/whitespace.py
And add it to your PATH variable:
export PATH=/path/to/whitespace.py:$PATH

Currently, marking it as a standalone executable on Windows is not implemented. As the Python documentation  suggests, the standard Python installer associates .py with the Python interpreter, and executes it automatically from the terminal. If you want to just type 'whitespace', you will need to add .py to $PATHEXT.

What works:
The program will accept both relative and absolute file paths for the input file.in, and strip whitespace and comments out and write it to file.out. It may do so rather slowly and more memory-intensively for larger files.
It makes use of the regex library that is native to Python.

What doesn't work:
If you have a very large file, your computer may hang for a while. If you have a REALLY large file, the program may actually crash. This has not been tested with arbitrarily large inputs.
This is because the file keeps the entire input in memory until it is finished, and creates another copy of the input bereft of whitespace and strings; little if any garbage collection occurs until the file is actually done.
Additionally, this script DOES NOT check if the file is readable, or even actually ends in .in. So if you attempt to read any arbirary file, the program will probably not work, and may make your input file rather unhappy, since it uses Python's 'read' rather than 'read binary'.
Furthermore, some whitespace between certain instructions may be lost.
For example:
(LOOP) @i
get smashed into
(LOOP)@i