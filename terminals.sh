#!/bin/sh



tmux new-session -d -s terminals 'bash'
tmux send-keys 'echo "first window"' 'C-m'
tmux send-keys 'tmux source-file ./scripts/tmux.log.config' 'C-m'
tmux rename-window 'main'
tmux select-window -t main
tmux split-window -h 'bash'
tmux send-keys 'echo "second window"' 'C-m'
tmux split-window -v -t 0 'bash'
tmux send-keys 'echo "third window"' 'C-m'
tmux split-window -v -t 1 'bash'
tmux send-keys 'echo "forth window"' 'C-m'
tmux -2 attach-session -t terminals
