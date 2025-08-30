#!/bin/bash
# Start FastAPI backend
cd ../backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 &

# React Native app deployment instructions
# For Android: cd ../frontend && npx react-native run-android
# For iOS: cd ../frontend && npx react-native run-ios
# Make sure to set up your environment for mobile development.
