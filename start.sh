#!/bin/bash

# Function to cleanup background processes on script termination
cleanup() {
    echo "Shutting down servers..."
    kill $(jobs -p) 2>/dev/null
    exit
}

# Set up trap for cleanup on script termination
trap cleanup SIGINT SIGTERM

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed"
    exit 1
fi

# Start the backend server
echo "Starting backend server..."
python3 -m uvicorn app:app --reload --port 8000 &
BACKEND_PID=$!

# Start the frontend development server
echo "Starting frontend server..."
cd frontend
if [ $? -ne 0 ]; then
    echo "Error: Could not find frontend directory"
    kill $BACKEND_PID
    exit 1
fi

npm start &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID 