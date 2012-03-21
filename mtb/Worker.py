import glob, threading, Queue, sys, shutil, time, os.path
from subprocess import call


class Worker(threading.Thread):
    dest = "/temp/backup_test"
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.daemon=True
        self._q = q
    def run(self):
        #enter loop
        while True:
            # get something off the queue i
            # (will block forever if neccessary)
            (srcFile, relDir) = self._q.get()
            if not os.path.isfile(srcFile):
                self._q.task_done()
                continue
            destDir  = self.dest + os.sep + relDir
            (srcRoot, srcFilename) = os.path.split(srcFile)
            destFile = destDir + os.sep + srcFilename
            if not os.path.exists(destDir):
                try:
                    # makedirs not thread safe be prepared for exception
                    # if another thread has already created this dir
                    os.makedirs(destDir, 0755) 
                except OSError, err: 
                    if err.errno==17: #file exists 
                        # someone else has created the directory in the 
                        # meantime. That's fine with me! 
                        pass 
                    else: 
                        raise
            print '{}: Copying from {} to {}'.format(self.name, srcFile, destFile)
            try:
                #shutil.copy2(srcFile, destFile)
                # rsync options explained:
                #   t: preserves and check mtime of files and only transfers out of date files
                #   l: preserves symlinks
                #   p: preserve permissions
                #   g: preserve group
                #   o: preserve owner
                call(['/usr/bin/rsync', '-tlpgo', srcFile, destFile])
            except IOError as e:
                print '   ... Skipping: {}'.format(e)
            self._q.task_done()

