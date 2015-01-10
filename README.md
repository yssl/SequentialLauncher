# sequential_logging_launcher.py

An automation script for launching a sequence of CLI processes while logging their stdout and stderr to a file.

## Usage
Pass launching commands as a command line argument in the form of "python list" in double quotes.  

Examples:
```
  $ python sequential_logging_launcher.py "['ls','ls -al','ls -R /','ls']"
```
