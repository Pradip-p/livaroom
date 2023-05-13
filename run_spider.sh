#!/bin/bash
cd /root/livaroom/
/usr/bin/env bash -c 'source /root/livaroom/tools/bin/activate && /root/livaroom/tools/bin/python /root/livaroom/crawler/livaroom_com.py'

/usr/bin/env bash -c 'source /root/livaroom/tools/bin/activate && /root/livaroom/tools/bin/python /root/livaroom/crawler/english.py'


#save the files  .....
0 0 * * * source /root/livaroom/tools/bin/activate && /root/livaroom/crawler/livaroom_com.py >> /root/logs/crons.log 2>&1
0 0 * * * source /root/livaroom/tools/bin/activate && /root/livaroom/crawler/english.py >> /root/logs/crons.log 2>&1
