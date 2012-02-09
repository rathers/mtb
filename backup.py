#! /usr/bin/env python

# todo
#  - store tuples in the queue to store relarive path alongside absolute path
#  - derive decent list of files
#  - rsynch support
#  - hook into s3fs


# should imports go at the top of a file as a good convention?
# doesnt seem very 'pythonic'
import glob, threading, Queue, sys, shutil, time, os.path


class Worker(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.daemon=True
        self._q = q
    def run(self):
        #enter loop
        while True:
            # get something off the queue i
            # (will block forever if neccessary)
            source = self._q.get()
            if not os.path.isfile(source):
                self._q.task_done()
                continue
            print '{}: {}'.format(self.name, source)
            try:
                #shutil.copy2(source,'/temp/backup_test/')
                a=1
            except IOError as e:
                print '   ... Skipping: {}'.format(e)
            self._q.task_done()

class Producer(object):
    def __init__(self, q):
        self._q = q
    def start(self):
        noThreads=5
        # create N worker threads to consume the queue
        self.startWorkers(noThreads, self._q)
        self.readFilesFile('files.txt', self._q)
        self.waitForEnd(self._q)
    def waitForEnd(self, q):
        while q.empty() != True:
            time.sleep(1)
        q.join()
    def startWorkers(self, count, q):
        for i in range(0,count):
            w = Worker(q)
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
            if os.path.isdir(path):
                os.path.walk(path, self.processDir, (q, path))
            else:
                self.putWithRetry(path, q)
    def processDir(self, (q,origPath), dirname, names):
        (root,basename) = os.path.split(origPath)
        relDir = os.path.relpath(dirname, root)
        for f in names:
            fqPath = os.path.join(dirname, f)
            print 'Got {}, {}'.format(relDir, fqPath)
            if os.path.isdir(fqPath):
                continue
            self.putWithRetry(fqPath, q)
    def putWithRetry(self, path, q):
        while True:
            try:
                q.put(path, True, 1)
                break
            except Queue.Full:
                a=1

#time.sleep(1)
queueSize=1000
# create a FIFO queue to put file paths into
q = Queue.Queue(queueSize)
# create N worker threads to consume the queue
p = Producer(q)
p.start()

#for i in range(0,noThreads):
#    w = Worker(q)
#    w.start()
#producer(q)
#q.join()


