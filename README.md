# MTB - Multi-Threaded Backup

## Introduction
[Amazon S3](http://aws.amazon.com/s3/) provides an excellent solution for off-site backups, delivering resilience and scalability for relatively little cost.

[S3FS](http://code.google.com/p/s3fs/) provides a way to mount an S3 bucket into your linux filesystem making it very easy to use standard linux tools such as cp and rsync to make offsite backups of your files. Communicating over S3 with  a domestic braodband connection however can be slow due to network latency. Based on [research by Marcus Rasmussen](http://improve.dk/archive/2011/11/07/pushing-the-limits-of-amazon-s3-upload-performance.aspx) it is possible to significantly increase write throughput to S3 by running several upload processes in parallel. MTB seeks to make this task simple by synching a set of files on your local machine with your S3 bucket using multiple parallel upload threads.

In short MTB allows to backup to S3, fast.

## Architecture

MTB is a python script that you can run from the command line. You pass it a few simple pieces of information such as:

* A file that contains a list of the files/directories you want to backup
* The location of your S3 bucket mounted using S3FS
* The number of worker threads to spawn

MTB then parses the input file and compiles a list of all the individual files it needs to synch up to S3. It places these items into a queue and spawns multiple worker threads that pick files off the queue and synch them one at a time. Synching is done using rsync so files will only be uploaded to S3 if they have changed. Still the process of calculating whether or not a file needs to be transferred still requires network comms and this is where MTB's parallelisation can help speed thigns up.

## Status

It isnt finished yet! Use at your peril! :)

Also this is my fist foray into python so please excuse any tardiness and anti-pythonic behaviours!

## Usage

## Performance

https://docs.google.com/spreadsheet/ccc?key=0AnGF7GAs4sjAdGV4VjJ6VjlqZllwYXkwQkxrbnlxb3c
