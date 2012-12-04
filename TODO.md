== Features==
* ~~Get it working with S3
** ~~s3fs doesnt appear to be multi threaded so isnt much use :(
** ~~try s3cmd instead
** ~~possibly abandon project and work on adding multi-threading to s3cmd instead?
* Adapt ~/.mtb to be config/ini file like so i can have:
** multiple destinations
** dest directory mount commands/checks (for mounting s3fs and external HD)
** specififed no workers for destination (very few for local disk, many for s3)
* Make sure project structure in standards compliant
* setup.py

== Bugs ==
* Using more threads than there are files to copy resorts in the programmign terminating prematurely

== Performance ==
* Calling s3cmd seperately for each file is inefficient:
** uploading 100 1KB files in one call took 23s
** The same files as separate calls took 36s
** Investigate options here
*** Find out what is causing the delay
**** option parsing?
**** process creation?
**** connection establishment?
**** file stat-ing?
*** Can i short cut the inefficiency?
*** Should i make s3cmd multi-threaded?
*** Can i just use the S3 library directly? What am i losing out on of i do?
