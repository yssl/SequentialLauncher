# sequential_logging_launcher.py

This script allows you to automate launches of any command line interface processes while logging all their output to a file.

## Features
- Automating sequential execution of any type, any number of command line interface processes.
- Logging all output (stdout and stderr) of the subprocesses to a file per execution of this script (default location: ~/sequential_logging_launcher_log/).
- Logging the start, end, and elapsed time of each subprocess and the whole script.
- Reporting succeeded / falied subprocesses in the final summary, by checking the return code and raised exceptions of each subprocess.
- Inserting a prefix at the beginning of each ouput line to show which command is currently processing.

## Usage
Pass your launching commands as a command line argument in the form of [python list](http://www.tutorialspoint.com/python/python_lists.htm), in double quotes.  

Examples:
```
$ python sequential_logging_launcher.py "['ls -al','ps -afx','this will fail','ls']"
```

###### Todo
- command line argument options
  - set log dir
  - set flushing for each single line or not (or number of lines until flushing)
