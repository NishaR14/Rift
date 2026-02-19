#!/bin/bash

# Start script for PharmaGuard
# Starts both backend and frontend

echo "Starting PharmaGuard..."

# Start backend in background
cd backend
python app.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
npm run dev

# Cleanup on exit
trap "kill $BACKEND_PID" EXIT
