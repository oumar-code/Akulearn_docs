#!/bin/bash
# Akulearn Client App Deployment Script

JAR_PATH="build/libs/akulearn-client.jar"
TARGET_DEVICE="pi@192.168.1.100"

# Copy JAR to device
scp $JAR_PATH $TARGET_DEVICE:~/akulearn-client.jar

# Start app remotely
ssh $TARGET_DEVICE 'java -jar ~/akulearn-client.jar &'

echo "Deployment complete."
