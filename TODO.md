== Features==
* Get it working with S3
** s3fs doesnt appear to be multi threaded so isnt much use :(
** try s3cmd instead
** possibly abandon project and work on adding multi-threading to s3cmd instead?
* Adapt ~/.mtb to be config/ini file like so i can have:
** multiple destinations
** dest directory mount commands/checks (for mounting s3fs and external HD)
** specififed no workers for destination (very few for local disk, many for s3)
* Make sure project structure in standards compliant
* setup.py

== Bugs ==
* Using more threads than there are files to copy resorts in the programmign terminating prematurely

