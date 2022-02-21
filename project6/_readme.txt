How to compile:

You don't really need to compile Python, but if you do want bytecode, you can run from a terminal with Python (from the directory that assembler.py is in):
python3 -m py_compile assembler.py (Unix)
python -m py_compile assembler.py (Windows Powershell)
or use the provided compile.py file in your development environment (your workspace must be the directory of whitespace.py for it to work, so use the terminal instead).
The bytecode file has the extension .pyc, and is found in a folder labeled "__pycache__" inside src.

py_compile is a standard Python library package and does not need installing.

How to run:

From your command line, with Python installed:
Windows Powershell:
python path\to\assembler.py path\to\input_file.asm (should just default to python3)
Unix terminal:
python3 path/to/assembler.py path/to/input_file.asm (DO NOT use python2; it probably won't work, and has NOT been tested.)
For relative paths, you may need to enclose your input path in a string.

On Unix, the file already has the shebang header to mark it as executable. If you wish to make it so, run the following:
chmod +x path/to/assembler.py
And add it to your PATH variable:
export PATH=/path/to/assembler.py:$PATH

Currently, marking it as a standalone executable on Windows is not implemented. As the Python documentation  suggests, the standard Python installer associates .py with the Python interpreter, and executes it automatically from the terminal. If you want to just type 'assembler', you will need to add .py to $PATHEXT.

What works:
The program will accept .asm files and automatically compile them into .hack machine code, and will automatically keep the existing file names and port them over. It makes use of the regex library.

What doesn't work:
This program does not check if .asm files actually make any sense, and will abort halfway with arcane Python error messages instead. Additionally, it will try to convert ALL files you type in as long as they're valid, even if they don't end in .asm, and will probably spew out useless garbage, if not crash.
The new version uses pathlib instead of os.path, but might still be broken; it attempts to go around by taking your input and forcibly converting it to an absolute path.