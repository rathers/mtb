import glob, threading, Queue, sys, shutil, time, os.path, logging
from mtb.Worker import Worker

class Producer(object):
    noThreads = 15
    def __init__(self, q, log):
        self._q = q
        self.log = log
    def start(self):
        # create N worker threads to consume the queue
        self.startWorkers(self.noThreads, self._q, self.log)
        self.readFilesFile(os.path.expanduser('~/.mtb'), self._q)
        self.waitForEnd(self._q)
    def waitForEnd(self, q):
        while q.empty() != True:
            time.sleep(1)
        q.join()
    def startWorkers(self, count, q, log):
        for i in range(0,count):
            w = Worker(q, log)
            w.start()
    def readFilesFile(self, path, q):
        with open(path) as backupListFile:
            for line in backupListFile:
                # remove trailing carriage return
                line = line.rstrip()
                self.processLine(line, q)
    def processLine(self, line, q):
        # resolves wildchars in the path
        resolvedPaths = glob.glob(line)
        for path in resolvedPaths:
            # it's a directory
            if os.path.isdir(path):
                # walk the direcotry passing the original path 
                # and the queue to the walker function as a tuple
                os.path.walk(path, self.processDir, (q, path))
            # it's just a file
            else:
                self.putWithRetry(path, "", q)
    def processDir(self, (q,origPath), dirname, names):
        # queue and origPath unpacked frm tuple
        # split FQP on original filename that was found in the files file
        (root,basename) = os.path.split(origPath)
        # now find relative path. 
        # This will ultimatey be used as the dir path in s3
        relDir = os.path.relpath(dirname, root)
        for f in names:
            fqPath = os.path.join(dirname, f)
            #print 'Got {}, {}'.format(relDir, fqPath)
            # not interested in blank directories
            if os.path.isdir(fqPath):
                continue
            # shove on queue
            self.putWithRetry(fqPath, relDir, q)
    def putWithRetry(self, fqPath, relDir, q):
        while True:
            try:
                q.put((fqPath, relDir), True, 1)
                self.log.debug("[queue-on] " + fqPath)
                break
            except Queue.Full:
                a=1

