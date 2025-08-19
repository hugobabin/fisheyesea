#!/bin/bash

SESSION_NAME="fisheyesea"

# Kill existing session if it exists
tmux has-session -t $SESSION_NAME 2>/dev/null
if [ $? -eq 0 ]; then
    echo "Killing existing tmux session: $SESSION_NAME"
    tmux kill-session -t $SESSION_NAME
fi

# Start new session in detached mode
tmux new-session -d -s $SESSION_NAME

# Run backend in first pane
tmux send-keys -t $SESSION_NAME "uv run fastapi dev main.py" C-m

# Split window horizontally and run frontend
tmux split-window -h -t $SESSION_NAME
tmux send-keys -t $SESSION_NAME "cd frontend && npm run dev" C-m

# Split right window vertically and run docker-compose
tmux split-window -v -t $SESSION_NAME
tmux send-keys -t $SESSION_NAME "cd db && docker-compose up -d --build" C-m

# Attach to session
tmux attach -t $SESSION_NAME
