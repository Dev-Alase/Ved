#!/bin/bash
LOG_FILE="logs/k8s.log"
mkdir -p logs
kubectl logs test-pod -n devpulse --tail=1000 >> $LOG_FILE