#!/bin/sh



tmux new-session -d -s dev 'bash'
tmux send-keys 'export PS1="> "' 'C-m'
tmux send-keys 'tmux source-file ./scripts/tmux.log.config' 'C-m'
tmux send-keys 'clear' 'C-m'
tmux send-keys 'echo "first window"' 'C-m'
tmux send-keys 'kubectl logs -f deployment/flask' 'C-m'
tmux rename-window 'main'
tmux select-window -t main
tmux split-window -h 'bash'
tmux send-keys 'export PS1="> "' 'C-m'
tmux send-keys 'clear' 'C-m'
tmux send-keys 'kubectl logs -f deployment/web' 'C-m'
tmux split-window -v -t 0 'bash'
tmux send-keys 'export PS1="> "' 'C-m'
tmux send-keys 'clear' 'C-m'
tmux send-keys 'kubectl logs -f deployment/db' 'C-m'
tmux split-window -v -t 1 'bash'
tmux send-keys 'export PS1="> "' 'C-m'
tmux send-keys 'clear' 'C-m'
tmux send-keys 'echo "forth window"' 'C-m'
tmux -2 attach-session -t dev
