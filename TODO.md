## Features
* Adapt ~/.mtb to be config/ini file like so i can have:
** multiple destinations
** dest directory mount commands/checks (for mounting external HD)
** specififed no. workers for destination (very few for local disk, many for s3)
* Make sure project structure is standards compliant
* setup.py

## Bugs 
* Using more threads than there are files to copy resorts in the programmign terminating prematurely
* trailing slash on the end of a directory in the files file causes the remote directory to become '.'

## Refactoring
* Move Worker spawning code out of Producer (no idea why I put it there in the first place!)
