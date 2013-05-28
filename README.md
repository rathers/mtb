# MTB - Multi-Threaded Backup

## Introduction
[Amazon S3](http://aws.amazon.com/s3/) provides an excellent solution for off-site backups, delivering resilience and scalability for relatively little cost. Based on [research by Marcus Rasmussen](http://improve.dk/archive/2011/11/07/pushing-the-limits-of-amazon-s3-upload-performance.aspx) it is possible to significantly increase write throughput to S3 by running several upload processes in parallel. MTB seeks to make this task simple by synching a set of files on your local machine with your S3 bucket using multiple parallel upload threads.

In short MTB allows to backup to S3, fast.

## Architecture

MTB is a simple python command line application. Simply provide it with a list of files and/or directories that you want to backup and it will take care of the rest. It is built using the python AWS library [Boto](https://github.com/boto/boto) and utilises the python threading library to implement concurrency. A Producer process searches for the files you wish to backup and adds each one as a job to a queue. Multiple Worker threads then read jobs off the queue and back up each file in turn. The modified time of the file is checked against the one held on S3 and the file is only uploaded if the time has been changed locally. In this respect it behaves like rsync.

Because the process of checking modified times and uploading small files involves a lot of network wait, multiple worked can significantly speed up the process and better utilise your upstream bandwidth. The more latency in your connection to S3 the more you will benefit from multiple threads.

## Status

MTB has been reasonably well tested using my personal setup which is as follows:

* Arch Linux 32-bit
* Python 2.7.3
* S3 Bucket in eu-west

I know of no reason why it would not function on a unix-like system with a modern verison of python installed but I have used a few unix-specific things so you may have trouble on Windows, sorry!

Also this is my fist foray into python so please excuse any tardiness and anti-pythonic behaviours!

## Setup

* Download the source to somewhere on your machine
* [Install boto](https://github.com/boto/boto#installation)
* Create an MTB config file at ~/.mtb that contains a list of files and directories you want to backup. Each path on a separate line. For example:

```
    /home/rathers/music
    /home/rathers/documents/cv.doc
```
* Create a boto config file in order that we can connect to your S3 bucket. [This page](http://code.google.com/p/boto/wiki/BotoConfig) explains how to do this. I have a config file at /etc/boto.cfg with the following contents:

```ini
[Credentials]
aws_access_key_id = XXXXXXXXXXXXXXXXXXXX
aws_secret_access_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
[Boto]
debug = 0
num_retries = 2
http_socket_timeout = 1000
```

## Usage

Once everything is configured as above all you need to do is run the mtb application:

./bin/mtb
