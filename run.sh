#!/bin/bash

JENKINS_SSH_PATH=$1

nohup python3.9 $JENKINS_SSH_PATH/run_chat_api_server.py >> $JENKINS_SSH_PATH/nohup.out  2>&1 &
