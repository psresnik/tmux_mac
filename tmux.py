import csv
import json
import os
import sys
import subprocess
import stat
import secrets

# Where to find list of sessions to start up
# This should be the same file that tmux-session saves its info to
# (TAB-separated session name, window name, directory)
homedir    = os.environ.get("HOME")
sessions_file = f"{homedir}/.tmux-session"


def make_executable(file_path):
    mode = os.stat(file_path).st_mode
    os.chmod(file_path, mode | stat.S_IEXEC)

def read_sessions(file_path):
    """Read the sessions file and return a dictionary of sessions with their windows and directories."""
    sessions = {}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile,delimiter='\t')
        for row in reader:
            session = row['Session']
            if session not in sessions and session.strip(): # Also making sure it's not all whitespace
                sessions[session] = []
            sessions[session].append((row['Window'], row['Dir']))
    return sessions

def execute_command_in_new_terminal(cmd,session):
    
    # Create a unique temporary file in /tmp
    # Session name will appear in window title
    temp_file = f"/tmp/DEL_TMUX_{session}_" + str(secrets.randbits(40))
    with open(temp_file, 'w') as file:
        file.write("#!/bin/bash\n")  # Specify /bin/bash as the shell
        file.write(cmd + "\n")       # Write the command to the temporary file

    # Make the temporary file executable
    make_executable(temp_file)
    
    # Use osascript to create new terminal window in which the temporary file is executed
    # https://superuser.com/questions/174576/opening-a-new-terminal-from-the-command-line-and-running-a-command-on-mac-os-x#308460
    script = "tell app \"Terminal\" to do script " + "\"" + temp_file + "\""
    print(script)
    subprocess.run(['osascript','-e',script])

    # Note: CAN'T os.remove() the temporary file right away since the new terminal
    # window may not have gotten around to executing it yet (race condition).
    # Instead, leave it in /tmp.
    #  os.remove(temp_file) # DEBUG
    
def start_sessions(sessions):
    """Get each session started in a new terminal window"""
    
    for session, windows in sessions.items():

        s = ''
        
        # Build command string: Start the tmux session...
        s += f"tmux new-session -s \"{session}\" -n \"{session}\" \\; "
        
        # ...Iterate over windows and directories
        for window, dir in windows:
            s += f"new-window -n '{window}' \\; "
            s += f"send-keys 'cd {dir}' C-m 'pwd' C-m \\; "

        # ...Select the first window
        # ...Super-kludgy: the tmux new-session created a window 0 that we don't want, so kill it
        # ...Clear the terminal window
        # POSSIBLY TO DO: Save and restore env? History?
        # POSSIBLY TO DO: Create process that saves sessions cron-like, but without needing cron
        s += f"select-window -t 1 \\; "
        s += f"send-keys 'tmux kill-window -t 0' C-m \\; "
        s += f"send-keys 'clear' C-m"
        s += f"\n"

        print(f"Starting session {session}") 
        execute_command_in_new_terminal(s,session)

def main():
    
    sessions = read_sessions(sessions_file)
    start_sessions(sessions)
    print("Done. To clean up temp files: rm /tmp/DEL_TMUX_*")

if __name__ == "__main__":
    main()
