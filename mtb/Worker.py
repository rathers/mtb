import glob, threading, Queue, sys, shutil, time, os.path, logging
from subprocess import call
from boto.s3.key import Key
from boto.s3.connection import S3Connection


class Worker(threading.Thread):
    #dest = "/temp/backup_test"
    dest = ""
    def __init__(self, q, log):
        threading.Thread.__init__(self)
        self.daemon=True
        self._q = q
        self.log = log
    def run(self):
        #enter loop

        conn = S3Connection()
        bucket = conn.get_bucket('rathers-backup')
        while True:
            # get something off the queue i
            # (will block forever if neccessary)
            (srcFile, relDir) = self._q.get()
            if not os.path.isfile(srcFile):
                self._q.task_done()
                continue
            destDir  = [self.dest,relDir]
            (srcRoot, srcFilename) = os.path.split(srcFile)

            destFile = destDir[:] # create a copy of list
            destFile.append(srcFilename)

            sDestDir  = os.sep.join(filter(None,destDir))
            sDestFile = os.sep.join(filter(None,destFile))

           #if not os.path.exists(destDir):
           #    try:
           #        # makedirs not thread safe be prepared for exception
           #        # if another thread has already created this dir
           #        os.makedirs(destDir, 0755) 
           #    except OSError, err: 
           #        if err.errno==17: #file exists 
           #            # someone else has created the directory in the 
           #            # meantime. That's fine with me! 
           #            pass 
           #        else: 
           #            raise
            self.log.info('Copying from {} to {}'.format(srcFile, sDestFile))
            try:
                fileStat = os.stat(srcFile)
                localMTime = int(fileStat.st_mtime)
                key = bucket.get_key(sDestFile)
                upload = False
                if key == None:
                    key = bucket.new_key(sDestFile)
                    upload = True
                    self.log.info("New file!!")
                else:
                    remoteMTime = key.get_metadata("mtime")
                    if  (remoteMTime != None) and (int(remoteMTime) != localMTime):
                        upload = True
                        self.log.info("file changed ({}, {}), uploading {}".format(localMTime, remoteMTime, srcFile))

                if upload == True:
                    key.set_metadata("mtime", str(localMTime))
                    key.set_contents_from_filename(srcFile)
                else:
                    self.log.info("File unchanged, skipping...")

            except IOError as e:
                self.log.warn('IOError, skipping {}: {}'.format(srcFile, e))
                self._q.task_done()
                #self._q.put((srcFile, relDir))
                continue
            except Exception as e:
                #assume boto exception
                self.log.warn('Boto Error, skipping, but will retry {}: {}'.format(srcFile, e))
                self._q.task_done()
                self._q.put((srcFile, relDir))
                continue
            self.log.debug("[queue-off] " + srcFile)
            self._q.task_done()

