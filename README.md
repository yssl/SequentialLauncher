# SequentialLauncher.py

This script allows you to automate launches of any command line interface processes while logging all their output to a file.

## Features
- Automating sequential execution of any type, any number of command line interface processes.
- Logging all output (stdout and stderr) of the subprocesses to a file per execution of this script (default location: ~/SequentialLauncherLog/).
- Logging the start, end, and elapsed time of each subprocess and the whole script.
- Reporting succeeded / falied subprocesses in the final summary, by checking the return code and raised exceptions of each subprocess.
- Inserting a prefix at the beginning of each ouput line to show which command is currently processing.

## Usage
Pass your launching commands as a command line argument in the form of [python list](http://www.tutorialspoint.com/python/python_lists.htm), in double quotes.  
```
$ ./SequentialLauncher.py -h
usage: SequentialLauncher.py [-h] [-l LOG_DIRECTORY] commands

Automates launches of any command line interface processes, logs all their
output to a file.

positional arguments:
  commands              commands string in the form of python list in double
                        quote

optional arguments:
  -h, --help            show this help message and exit
  -l LOG_DIRECTORY, --log-directory LOG_DIRECTORY
                        specify the LOG_DIRECTORY in which log files to be
                        generated
```

## Example
```
$ ./SequentialLauncher.py "['ls -al','ps -afx','this will fail','ls']"
================================================================================
SequentialLauncher.py
- Automates launches of any command line interface processes and logs all their output to a file.

STARTED at 2015-01-14 23:44:13.671808
Executed in /media/sda1/Work/SequentialLauncher.py

# of total launching commands: 4
1> ls -al
2> ps -afx
3> this will fail
4> ls
================================================================================

============================================================
1> ls -al
1> STARTED at 2015-01-14 23:44:13.673345
============================================================

1> total 24
1> drwxrwxr-x 3 testid testid 4096  Jan 14 23:42 .
1> drwx------ 5 testid testid 4096  Jan  9 02:53 ..
1> drwxrwxr-x 8 testid testid 4096  Jan 14 23:44 .git
1> -rw-rw-r-- 1 testid testid 1165  Jan 14 23:42 README.md
1> -rw-rw-r-- 1 testid testid 5074  Jan 14 23:42 sequential_logging_launcher.py

============================================================
1> ls -al
1> SUCCEEDED at 2015-01-14 23:44:13.680078
1> Elapsed time: 0:00:00.006733
============================================================

============================================================
2> ps -afx
2> STARTED at 2015-01-14 23:44:13.680250
============================================================

2>   PID TTY      STAT   TIME COMMAND
2>     2 ?        S      0:00 [kthreadd]
2>     3 ?        S      0:02  \_ [ksoftirqd/0]
2>     5 ?        S<     0:00  \_ [kworker/0:0H]
(...)

============================================================
2> ps -afx
2> SUCCEEDED at 2015-01-14 23:44:13.712912
2> Elapsed time: 0:00:00.032662
============================================================

============================================================
3> this will fail
3> STARTED at 2015-01-14 23:44:13.713027
============================================================

3> /bin/sh: 1: this: not found

============================================================
3> this will fail
3> FAILED at 2015-01-14 23:44:13.714581
3> Elapsed time: 0:00:00.001554
============================================================

============================================================
4> ls
4> STARTED at 2015-01-14 23:44:13.714659
============================================================

4> README.md
4> SequentialLauncher.py

============================================================
4> ls
4> SUCCEEDED at 2015-01-14 23:44:13.721384
4> Elapsed time: 0:00:00.006725
============================================================

================================================================================
SequentialLauncher.py

FINISHED at 2015-01-14 23:44:13.721564
Elapsed time: 0:00:00.049756

# of succeeded launching commands: 3
1> ls -al
2> ps -afx
4> ls

# of failed launching commands: 1
3> this will fail
================================================================================

This log has been saved to /home/testid/SequentialLauncherLog/2015-01-14--23-44-13.txt
```
