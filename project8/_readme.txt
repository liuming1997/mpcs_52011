How to compile:

You don't really need to compile Python, but if you do want bytecode, you can run from a terminal with Python (from the directory that vmtranslator.py is in):
python3 -m py_compile vmtranslator.py( Unix)
python -m py_compile vmtranslator.py (Windows Powershell)
or use the provided compile.py file in your development environment (your workspace must be the directory of vmtranslator.py for it to work, so use the terminal instead).
The bytecode file has the extension .pyc, and is found in a folder labeled "__pycache__" inside src.

py_compile is a standard Python library package and does not need installing.

How to run:

From your command line, with Python installed:
Windows Powershell:
python path\to\vmtranslator.py path\to\input_file.vm (should just default to python3)
Unix terminal:
python3 path/to/vmtranslator.py path/to/input_file.vm (DO NOT use python2; it will NOT work.)
For relative paths, you may need to enclose your input path in a string.

On Unix, the file already has the shebang header to mark it as executable. If you wish to make it so, run the following:
chmod +x path/to/assembler.py
And add it to your PATH variable:
export PATH=/path/to/assembler.py:$PATH

Currently, marking it as a standalone executable on Windows is not implemented. As the Python documentation  suggests, the standard Python installer associates .py with the Python interpreter, and executes it automatically from the terminal. If you want to just type 'assembler', you will need to add .py to $PATHEXT.

What works:
The program will accept .vm files and automatically compile them into .asm language, and will automatically keep the existing file names and port them over. It makes use of the regex library.

What doesn't work:

This program won't work with FibonacciElement or StaticsTest because there's some kind of issue with bootstrapping; I spent all night from 9pm to 5:30am and couldn't figure out what was wrong. It does however work for all other tests not involving those two. It seems likely that the writeCall() function has issues, but I can't pin anything down because the CPU emulator is frustratingly vague.

This program will try to convert ALL files you type in as long as they're valid, even if they don't end in .asm, and will probably spew out useless garbage, if not crash. I accidentally overwrote a test file while doing this earlier today.
The new version uses pathlib instead of os.path, and thus doesn't work for Python versions under 3.4, if you still use those.