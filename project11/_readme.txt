How to run:

From your command line, with Python installed:
Windows Powershell:
python path\to\jacktokenizer.py path\to\input_file.jack (should just default to python3)
Unix terminal:
python3 path/to/jacktokenizer.py path/to/input_file.jack (DO NOT use python2; it will NOT work.)
For relative paths, you may need to enclose your input path in a string.

On Unix, the file already has the shebang header to mark it as executable. If you wish to make it so, run the following:
chmod +x path/to/assembler.py
And add it to your PATH variable:
export PATH=/path/to/assembler.py:$PATH

Currently, marking it as a standalone executable on Windows is not implemented. As the Python documentation suggests, the standard Python installer associates .py with the Python interpreter, and executes it automatically from the terminal. If you want to just type 'assembler', you will need to add .py to $PATHEXT.

What works:
This file does take a .jack file, tokenizes it, and attempts to write it to a .vm file. Emphasis on "attempts".

What doesn't work:
All of the interpretive syntax should be correct, but for whatever reason it refuses to write the buffer stream to a file. I spend five hours troubleshooting it and still can't get down to why, but I think vmwriter.py is screwed up.