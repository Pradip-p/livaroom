#!/bin/bash
cd /root/livaroom/
/usr/bin/env bash -c 'source /root/livaroom/tools/bin/activate && /root/livaroom/tools/bin/python /root/livaroom/crawler/livaroom_com.py'

/usr/bin/env bash -c 'source /root/livaroom/tools/bin/activate && /root/livaroom/tools/bin/python /root/livaroom/crawler/english.py'
