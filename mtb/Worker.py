import glob, threading, Queue, sys, shutil, time, os.path, logging
from subprocess import call
from boto.s3.key import Key
from boto.s3.connection import S3Connection


class Worker(threading.Thread):
    #dest = "/temp/backup_test"
    dest = ""
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
            print '{}: Copying from {} to {}'.format(self.name, srcFile, sDestFile)
            try:
                #shutil.copy2(srcFile, sDestFile)
                # rsync options explained:
                #   t: preserves and check mtime of files and only transfers out of date files
                #   l: preserves symlinks
                #   p: preserve permissions
                #   g: preserve group
                #   o: preserve owner
                a=1

                #call(['/usr/local/bin/s3cmd', 'put', srcFile, 's3://rathers-backup/{}'.format(sDestFile)])
                conn = S3Connection()
                bucket = conn.get_bucket('rathers-backup')
                key = bucket.get_key(sDestFile)
                fileStat = os.stat(srcFile)
                localMTime = int(fileStat.st_mtime)
                remoteMTime = int(key.get_metadata("mtime"))
#                remoteSize = int(key.get_metadata("size"))
                if  remoteMTime != localMTime:
                    logging.debug("file changed ({}, {}), uploading {}".format(localMTime, remoteMTime, srcFile))
                    key.set_metadata("mtime", str(localMTime))
                    key.set_contents_from_filename(srcFile)
                else:
                    logging.debug("mtime does not differ for " + srcFile)

            except IOError as e:
                print '   ... Skipping: {}'.format(e)
            self._q.task_done()

