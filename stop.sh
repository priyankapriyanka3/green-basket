#!/bin/bash
# stop.sh — Stop ONLY the services started by start.sh (uses .pids file)
# IMPORTANT: Only kills PIDs recorded in .pids — never uses pkill/killall
# which could accidentally kill other processes (e.g. the SDLC backend server).

echo "Stopping GreenBasket AI services..."

if [ -f .pids ]; then
    while IFS= read -r pid; do
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            # Try graceful shutdown first (SIGTERM)
            kill "$pid" 2>/dev/null && echo "  Sent SIGTERM to PID $pid"
        fi
    done < .pids
    
    # Wait up to 10 seconds for graceful shutdown
    echo "  Waiting for graceful shutdown..."
    sleep 2
    
    # Force kill any remaining processes
    while IFS= read -r pid; do
        if [ -n "$pid" ] && kill -0 "$pid" 2>/dev/null; then
            echo "  Force stopping PID $pid"
            kill -9 "$pid" 2>/dev/null || true
        fi
    done < .pids
    
    rm -f .pids
    echo "All services stopped"
else
    echo "No .pids file found — services may not be running or were stopped already"
fi
