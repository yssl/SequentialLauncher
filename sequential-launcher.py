#!/usr/bin/env python
# File:         sequential-launcher.py
# Description:  Automates launches of any command line interface processes and logs all their output to a file.
# Author:       Yoonsang Lee <http://github.com/yssl>
# License:      MIT License
#
# Usage:
#   ex)
#   $ ./sequential-launcher.py "['ls -al','ps -afx','this will fail','ls']"
#   $ ./sequential-launcher.py "['ls -al']" --log-directory ~/test-log/
#   $ ./sequential-launcher.py "['ls -al']" --log-open-cmd "firefox -new-tab"
#   $ ./sequential-launcher.py "['ls -al']" --ssh-notify-address user@hostname:port

import sys, os, datetime, subprocess, traceback, argparse

###################################
# parse cmd args

parser = argparse.ArgumentParser(prog='sequential-launcher.py', description='Automates launches of any command line interface processes, logs all their output to a file.')
parser.add_argument('commands', nargs=1,
                    help='command strings in the form of python list in double quote')
parser.add_argument('--log-directory', default='~/SequentialLauncherLog/',
                    help='specify the LOG_DIRECTORY in which log files to be generated')
parser.add_argument('--log-open-cmd',
                    help='specify LOG_OPEN_CMD to open a log file when launching starts')
parser.add_argument('--ssh-notify-address',
                    help='specify user@hostname:port if you want to be notified when the job is finished')

args = parser.parse_args()
#print args
#exit()

log_directory = args.log_directory
log_open_cmd = args.log_open_cmd
ssh_notify_address = args.ssh_notify_address

###################################
# classes & functions
class MultiWriter:
    def __init__(self, *writers):
        self.writers = writers
    def write(self, text):
        for w in self.writers:
            w.write(text)
    def close(self, text):
        for w in self.writers:
            w.close(text)
    def flush(self):
        pass
    def close(self):
        pass

class DispFileWriter(MultiWriter):
    def __init__(self, filename, appending=True):
        self.logfile = file(filename, 'a' if appending else 'w')
        MultiWriter.__init__(self, sys.stdout, self.logfile)
    def flush(self):
        self.logfile.flush()
    def close(self):
        self.logfile.close()

class StdoutReplacer:
    def __init__(self, writer):
        self.stdout_saved = sys.stdout
        self.writer = writer
        self.on()
    def flush(self):
        self.writer.flush()
    def close(self):
        self.writer.close()
        self.off()
    def on(self):
        sys.stdout = self.writer
    def off(self):
        sys.stdout = self.stdout_saved

class DispFileStdoutReplacer(StdoutReplacer):
    def __init__(self, filename, appending=True):
        StdoutReplacer.__init__(self, DispFileWriter(filename, appending))

def execute(command, insertStr, writer):
    popen = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines_iterator = iter(popen.stdout.readline, "")
    for line in lines_iterator:
        print insertStr+line, # yield line
        writer.flush()
    retcode = popen.wait()
    return retcode

def getPrefix(i):
    return '%d> '%(i+1)

###################################
# main logic

log_directory = os.path.expanduser(log_directory)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

launchcmds = eval(args.commands[0])
cmdresults = [False]*len(launchcmds)

gstarttime = datetime.datetime.now()
logname = gstarttime.strftime('%Y-%m-%d--%H-%M-%S')
logpath = os.path.join(log_directory, logname+'.txt')
stdreplacer = DispFileStdoutReplacer(logpath)

print '================================================================================'
print 'SequentialLauncher'
print '- Automates launches of any command line interface processes and logs all their output to a file.'
print
print 'STARTED at %s'%gstarttime
print 'Executed in %s'%os.getcwd()
print
print '# of total launching commands: %d'%len(launchcmds)
for i in range(len(launchcmds)):
    print '%s%s'%(getPrefix(i), launchcmds[i])
print '================================================================================'
print

if log_open_cmd:
    subprocess.Popen(log_open_cmd.split()+[logpath])

if ssh_notify_address:
    tokens = ssh_notify_address.split(':')
    ssh_hostname = tokens[0]
    if len(tokens) > 1:
        ssh_port = int(tokens[1])
    else:
        ssh_port = 22

def printCmdEndMessage(i, success, starttime):
    endtime = datetime.datetime.now()
    print
    print '============================================================'
    print '%s%s'%(getPrefix(i), launchcmds[i])
    if success:
        print '%sSUCCEEDED at %s'%(getPrefix(i), endtime)
    else:
        print '%sFAILED at %s'%(getPrefix(i), endtime)
    print '%sElapsed time: %s'%(getPrefix(i), endtime-starttime)
    print '============================================================'
    print


for i in range(len(launchcmds)):
    starttime = datetime.datetime.now()
    try:
        print '============================================================'
        print '%s%s'%(getPrefix(i), launchcmds[i])
        print '%sSTARTED at %s'%(getPrefix(i), starttime)
        print '============================================================'
        print

        #retcode = os.system(launchcmds[i])
        retcode = execute(launchcmds[i], getPrefix(i), stdreplacer.writer)
        if retcode==0:
            cmdresults[i] = True
            printCmdEndMessage(i, True, starttime)
        else:
            printCmdEndMessage(i, False, starttime)
    except:
        print sys.exc_info()
        traceback.print_exc()
        printCmdEndMessage(i, False, starttime)

def getScriptEndMessage():
    s = ''
    endtime = datetime.datetime.now()
    s +=  '================================================================================'
    s += '\n'
    s +=  'SequentialLauncher'
    s += '\n'
    s += '\n'
    s +=  'FINISHED at %s'%endtime
    s += '\n'
    s +=  'Elapsed time: %s'%(endtime-gstarttime)
    s += '\n'
    s += '\n'
    s +=  '# of succeeded launching commands: %d'%cmdresults.count(True)
    s += '\n'
    for i in range(len(launchcmds)):
        if cmdresults[i]:
            s +=  '%s%s'%(getPrefix(i), launchcmds[i])
            s += '\n'
    s += '\n'
    s +=  '# of failed launching commands: %d'%cmdresults.count(False)
    s += '\n'
    for i in range(len(launchcmds)):
        if not cmdresults[i]:
            s +=  '%s%s'%(getPrefix(i), launchcmds[i])
            s += '\n'
    s +=  '================================================================================'
    s += '\n'
    s += '\n'
    s +=  'This log has been saved to %s'%logpath
    s += '\n'
    return s

scriptEndMessage = getScriptEndMessage()
print scriptEndMessage

stdreplacer.close()

if ssh_notify_address:
    import socket
    infoStr = '!!! Notification from %s\n\n'%socket.gethostname()
    infoStr += scriptEndMessage
    os.system('ssh -p %d %s export DISPLAY=:0;zenity --info --text="%s"'
                %(ssh_port, ssh_hostname, infoStr))
