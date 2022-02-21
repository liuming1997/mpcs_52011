How to run:

From your command line, with Python installed:
Windows Powershell:
python path\to\vmtranslator.py path\to\input_file.jack (should just default to python3)
Unix terminal:
python3 path/to/vmtranslator.py path/to/input_file.jack (DO NOT use python2; it will NOT work.)
For relative paths, you may need to enclose your input path in a string.

On Unix, the file already has the shebang header to mark it as executable. If you wish to make it so, run the following:
chmod +x path/to/assembler.py
And add it to your PATH variable:
export PATH=/path/to/assembler.py:$PATH

Currently, marking it as a standalone executable on Windows is not implemented. As the Python documentation suggests, the standard Python installer associates .py with the Python interpreter, and executes it automatically from the terminal. If you want to just type 'assembler', you will need to add .py to $PATHEXT.

What works:

The program will correctly output an XML file of all of the tokens.

What doesn't work:

The program will not correctly output an XML file of the the entire program, since writeStatement() is buggy and duplicates lines, and writeExpressionList() was not finished due to time.
I have been dealing with my roommate dropping from the MPCS program and leaving the country immediately and while that is not an excuse, and I do not mean it to be, it has been a rather rough two weeks.

I anticipate fixing it before next week's final assignment.