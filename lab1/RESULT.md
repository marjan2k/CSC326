

-----------------------------------------------BENCHMARK-----------------------------------------------------



This is ApacheBench, Version 2.3 <: 1528965 $>

Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/

Licensed to The Apache Software Foundation, http://www.apache.org/



Benchmarking 52.23.183.97 (be patient).....done





Server Software:        WSGIServer/0.1

Server Hostname:        52.23.183.97

Server Port:            8080



Document Path:          /?keywords=helloworld+foo+bar

Document Length:        1217 bytes



Concurrency Level:      18

Time taken for tests:   0.640 seconds

Complete requests:      100

Failed requests:        0

Total transferred:      148400 bytes

HTML transferred:       121700 bytes

Requests per second:    156.14 [#/sec] (mean)

Time per request:       115.278 [ms] (mean)

Time per request:       6.404 [ms] (mean, across all concurrent requests)

Transfer rate:          226.29 [Kbytes/sec] received



Connection Times (ms)

              min  mean[+/-sd] median   max

Connect:       34   41   3.8     40      50

Processing:    38   67  72.9     48     359

Waiting:       36   64  73.3     45     359

Total:         73  108  73.8     89     405



Percentage of the requests served within a certain time (ms)

  50%     89

  66%     94

  75%     96

  80%     98

  90%    104

  95%    391

  98%    398

  99%    405

 100%    405 (longest request)



-----------------------------------------------BENCHMARK-----------------------------------------------------



<b>Maximum number of connections that can be handled by the server before any connection drops = 18</b>


<b>Maximum number of requests per second (RPS) that can be sustained by the server when operating with maximum number of connections = 156</b>


<b>percentile of response time or latency per request:

average (50%) = 89 ms

99 percentile = 405 ms</b>



vmstat:

procs -----------memory---------- ---swap-- -----io---- -system-- ------cpu-----

 r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st

 1  0      0  20204  49488 319036    0    0     8    36   31   40  0  0 99  0  0



mpstat:

Linux 3.13.0-36-generic (ip-172-31-7-14) 10/26/2015 _x86_64_(1 CPU)



01:20:28 AM  CPU    %usr   %nice    %sys %iowait    %irq   %soft  %steal  %guest  %gnice   %idle

01:20:28 AM  all    0.41    0.09    0.19    0.27    0.00    0.01    0.01    0.00    0.00   99.02



iostat:

Linux 3.13.0-36-generic (ip-172-31-7-14) 10/26/2015 _x86_64_(1 CPU)



avg-cpu:  %user   %nice %system %iowait  %steal   %idle

           0.41    0.09    0.21    0.27    0.01   99.02



Device:            tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn

xvdap1            2.05         8.32        35.80     627357    2699452



dstat:

You did not select any stats, using -cdngy by default.

----total-cpu-usage---- -dsk/total- -net/total- ---paging-- ---system--

usr sys idl wai hiq siq| read  writ| recv  send|  in   out | int   csw 

  0   0  99   0   0   0|8521B   36k|   0     0 |   0     0 |  31    40 

  0   0 100   0   0   0|   0     0 |   0     0 |   0     0 |  11    15 

  0   0 100   0   0   0|   0     0 |   0     0 |   0     0 |   6     8 

  0   0 100   0   0   0|   0     0 |   0     0 |   0     0 |   5     6 

  0   0 100   0   0   0|   0     0 |   0     0 |   0     0 |   5     8 

  0   0 100   0   0   0|   0    32k|   0     0 |   0     0 |  10    17 

  0   0 100   0   0   0|   0     0 |   0     0 |   0     0 |   6     6 

  0   0 100   0   0   0|   0     0 |   0     0 |   0     0 |   6     8 

  0   0 100   0   0   0|   0     0 |   0     0 |   0     0 |   5     6 

  0   0 100   0   0   0|   0     0 |   0     0 |   0     0 |   6    10 


