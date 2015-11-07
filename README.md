# SequentialLauncher

This script allows you to automate launches of any command line interface processes while logging all their output to a file.

## Features
- Automating sequential execution of any type, any number of command line interface processes.
- Logging all output (stdout and stderr) of the subprocesses to a file (default location: ~/SequentialLauncherLog/).
- Logging the start time, end time, and elapsed time of each subprocess and the execution time for all subprocesses.
- Reporting result of each subprocess execution (SUCCEEDED / FAILED) in the final summary, by checking the return code and raised exceptions.
- Inserting a prefix (e.g., 1> ) at the beginning of each ouput line to show which command is currently processing.

## Usage
Pass your launching commands as a command line argument in the form of [python list](http://www.tutorialspoint.com/python/python_lists.htm), in double quotes.  
```
$ ./sequential-launcher.py -h
usage: sequential-launcher.py [-h] [--log-directory LOG_DIRECTORY]
                              [--log-open-cmd LOG_OPEN_CMD]
                              [--ssh-notify-address SSH_NOTIFY_ADDRESS]
                              commands

Automates launches of any command line interface processes, logs all their
output to a file.

positional arguments:
  commands              commands string in the form of python list in double
                        quote

optional arguments:
  -h, --help            show this help message and exit
  --log-directory LOG_DIRECTORY
                        specify the LOG_DIRECTORY in which log files to be
                        generated
  --log-open-cmd LOG_OPEN_CMD
                        specify LOG_OPEN_CMD to open a log file when launching
                        starts
  --ssh-notify-address SSH_NOTIFY_ADDRESS
                        specify user@hostname:port if you want to be notified
                        when the job is finished

```

## Example
```
$ ./sequential-launcher.py "['ls -al','ps -afx','this will fail','ls']"
================================================================================
SequentialLauncher
- Automates launches of any command line interface processes and logs all their output to a file.

STARTED at 2015-11-06 19:17:42.076626
Executed in /media/Work/Script-Config/bin-script

# of total launching commands: 4
1> ls -al
2> ps -afx
3> this will fail
4> ls
================================================================================

============================================================
1> ls -al
1> STARTED at 2015-11-06 19:17:42.076801
============================================================

1> total 60
1> drwxrwxr-x 3 yoonsang yoonsang  4096 11월  6 19:17 .
1> drwxrwxr-x 6 yoonsang yoonsang  4096 10월 28 18:41 ..
1> drwxrwxr-x 8 yoonsang yoonsang  4096 11월  6 19:17 .git
1> -rwxrwxr-x 1 yoonsang yoonsang  7103 11월  6 19:17 sequential-launcher.py

============================================================
1> ls -al
1> SUCCEEDED at 2015-11-06 19:17:42.079768
1> Elapsed time: 0:00:00.002967
============================================================

============================================================
2> ps -afx
2> STARTED at 2015-11-06 19:17:42.079871
============================================================

2>   PID TTY      STAT   TIME COMMAND
2>     2 ?        S      0:00 [kthreadd]
2>     3 ?        S      0:00  \_ [ksoftirqd/0]
2>     5 ?        S<     0:00  \_ [kworker/0:0H]
...

============================================================
2> ps -afx
2> SUCCEEDED at 2015-11-06 19:17:42.104800
2> Elapsed time: 0:00:00.024929
============================================================

============================================================
3> this will fail
3> STARTED at 2015-11-06 19:17:42.104905
============================================================

3> /bin/sh: 1: this: not found

============================================================
3> this will fail
3> FAILED at 2015-11-06 19:17:42.106736
3> Elapsed time: 0:00:00.001831
============================================================

============================================================
4> ls
4> STARTED at 2015-11-06 19:17:42.106878
============================================================

4> sequential-launcher.py

============================================================
4> ls
4> SUCCEEDED at 2015-11-06 19:17:42.109368
4> Elapsed time: 0:00:00.002490
============================================================

================================================================================
SequentialLauncher

FINISHED at 2015-11-06 19:17:42.109542
Elapsed time: 0:00:00.032916

# of succeeded launching commands: 3
1> ls -al
2> ps -afx
4> ls

# of failed launching commands: 1
3> this will fail
================================================================================

This log has been saved to /home/testid/SequentialLauncherLog/2015-11-06--19-17-42.txt
```
