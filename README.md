# Semi-Persistent TMUX Management on a MAC

The tmux package is great for managing lots of different things you're doing, similar to windows/tabs in a browser, but if you're using it for that locally on a laptop and you restart the machine (or it crashes), you're out of luck -- your local tmux sessions are gone.

This a homegrown package that addresses that problem in a no-frills way for a Mac. It easily allows you to store a record of your current tmux sessions and windows along with the current directory in each window, and to recreate those sessions and windows putting you back into the correct directory.

Note that this is only semi-persistent because it does not save/restore environments nor commandline histories.

Also note that this is only for local tmux. It has nothing to do with re-attaching remote sessions.

* tmalias      : show these tmux management commands
* tms          : save all current tmux sessions 
* tmr          : start Terminal windows with all saved tmux sessions
* tmk <session>: kill a specific session (does not kill its terminal window)
* tmka         : kill all sessions (does not kill terminal windows)
* tmns         : reminder of how to create a new session
* tmnw <window>: create a new window in the current session

# How to install

Put file `tmux.py` in your $HOME directory

Copy the following to your dot-shell file and source it, or start a fresh Terminal window to make sure the aliases are active.

For .bashrc (most people)
<pre>
alias tmalias="grep '# tm' ~/.tcshrc"
alias tms="~/tmux-session save ; echo 'SAVED SESSIONS'; echo '=============='; cat ~/.tmux-session"
alias tmr="python ~/tmux.py"
alias tmk="tmux kill-session -t"
alias tmka="pkill tmux ; tmux ls"
alias tmns="echo 'Execute in fresh window: tmux new-session -s 'session' -n 'session' replacing 'session' with session name'"
alias tmnw="tmux new window -n"
</pre>

For .cshrc or .tcshrc (for those of us who are old school)
<pre>
alias tmalias "grep '# tm' ~/.tcshrc"
alias tms ~/tmux-session save ; echo 'SAVED SESSIONS'; echo "=============="; cat ~/.tmux-session
alias tmr python ~/tmux.py
alias tmk tmux kill-session -t 
alias tmka pkill tmux ; tmux ls
alias tmns echo "Execute in fresh window: tmux new-session  -s 'session' -n 'session' replacing 'session' with session name "
alias tmnw tmux new window -n
</pre>


# How to use

* Create a set of tmux sessions and windows, or use a set you've already got.

* Periodically execute `tms` (tmux save) to save the windows and directories for your current tmux sessions. (E.g. get in the habit of executing `tms` after you change directories.)

* If you need to restore sessions, simply execute `tmr` (tmux restore) and it will re-open all the tmux windows you had and change to the directory you were in, as of the last time you saved.

* Note that running `tmr` creates files in /tmp that are not deleted automatically. When `tmr` has recreated all the sessions, it will output a reminder to clean up temp files: `rm /tmp/DEL_TMUX_*`.

* The various other aliases, e.g. `tmk`, etc. are for convenience.

# Things that it would be nice to add

* Saving and restoring each window's environment variables

* Saving and restoring each window's commandline history

* Also dealing with remote sessions






