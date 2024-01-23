#!/bin/bash

# 이전에 실행된 gunicorn 또는 flask run 프로세스를 중지합니다.
pkill -f 'gunicorn'
pkill -f 'flask run --host 0.0.0.0 --port 5000 --timeout 90 --debug'

# 로그 파일과 프로젝트 디렉터리를 초기화합니다.
rm -rf /home/ubuntu/gunicorn.log
rm -rf /home/ubuntu/ssg_backend
mkdir /home/ubuntu/ssg_backend

cd /home/ubuntu/ssg_backend || exit
