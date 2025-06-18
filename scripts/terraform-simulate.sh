#!/bin/bash
LOG_FILE="logs/terraform.log"
mkdir -p logs
echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"service\": \"terraform\", \"logLevel\": \"INFO\", \"message\": \"Planning infrastructure\", \"metadata\": {}}" >> $LOG_FILE
if [ $((RANDOM % 2)) -eq 0 ]; then
    echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"service\": \"terraform\", \"logLevel\": \"ERROR\", \"message\": \"Apply failed\", \"metadata\": {\"error_code\": \"invalid_config\"}}" >> $LOG_FILE
else
    echo "{\"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"service\": \"terraform\", \"logLevel\": \"INFO\", \"message\": \"Apply successful\", \"metadata\": {\"resources\": 2}}" >> $LOG_FILE
fi