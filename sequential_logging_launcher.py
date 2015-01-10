# File:         sequential_logging_launcher.py
# Description:  An automation script for launching a sequence of CLI processes while logging their stdout and stderr to a file.
# Author:       Yoonsang Lee <http://github.com/yssl>
# License:      MIT License
#
# Usage:
#   ex)
#   $ python sequential_logging_launcher.py "['ls','ls -al','ls -R /','ls']"

import sys, os, datetime, subprocess, traceback

logdir = '~/sequential_logging_launcher_log/'

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
logdir = os.path.expanduser(logdir)
if not os.path.exists(logdir):
    os.makedirs(logdir)

launchcmds = eval(sys.argv[1])
cmdresults = [False]*len(launchcmds)

gstarttime = datetime.datetime.now()
logname = gstarttime.strftime('%Y-%m-%d--%H-%M-%S')
logpath = os.path.join(logdir, logname+'.txt')
stdreplacer = DispFileStdoutReplacer(logpath)

print '================================================================================'
print 'sequential_logging_launcher.py v1.0.0'
print '- An automation script for launching a sequence of CLI processes'
print '  while logging their stdout and stderr to a file.'
print
print 'STARTED at %s'%gstarttime
print 
print '# of total launching commands: %d'%len(launchcmds)
for i in range(len(launchcmds)):
    print '%s%s'%(getPrefix(i), launchcmds[i])
print '================================================================================'
print

def printEndMessage(i, success, starttime):
    endtime = datetime.datetime.now()
    print
    print '============================================================'
    print '%s%s'%(getPrefix(i), launchcmds[i])
    if success:
        print '%sSUCCEEDED at %s'%(getPrefix(i), endtime)
    else:
        print '%sFAILED at %s'%(getPrefix(i), endtime)
    print '%sElapsed time : %s'%(getPrefix(i), endtime-starttime)
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
            printEndMessage(i, True, starttime)
        else:
            printEndMessage(i, False, starttime)
    except:
        print sys.exc_info()
        traceback.print_exc()
        printEndMessage(i, False, starttime)


endtime = datetime.datetime.now()
print
print '================================================================================'
print 'sequential_logging_launcher.py'
print
print 'FINISHED at %s'%endtime
print 'Elapsed time : %s'%(endtime-gstarttime)
print
print '# of succeeded launching commands: %d'%cmdresults.count(True)
for i in range(len(launchcmds)):
    if cmdresults[i]:
        print '%s%s'%(getPrefix(i), launchcmds[i])
print
print '# of failed launching commands: %d'%cmdresults.count(False)
for i in range(len(launchcmds)):
    if not cmdresults[i]:
        print '%s%s'%(getPrefix(i), launchcmds[i])
print '================================================================================'
print
print 'This log has been saved to %s'%logpath

stdreplacer.close()
