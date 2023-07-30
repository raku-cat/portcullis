<h1 align="center">
    Portcullis - An SSH "bouncer" written in Python
</h1>

<button>
    <img 
    src="https://github.com/raku-cat/portcullis/assets/1125449/f5c86125-240c-4139-bdf1-32162b787f62" 
    align="right"
    width="60%"
    />
</button>

<button>
    <dl>
        <dt><h3>Portcullis</h3></dt>
        <dd><em>n.</em> a strong, heavy grating that can be lowered down grooves on each side of a gateway to block it.</dd>
        </dl>
    <img
        src="https://github.com/raku-cat/portcullis/assets/1125449/255651ef-596a-47e9-b4aa-4f76fa836734"
        height="340px"
        width="38%"
    />
</button>

***

# About
Designed after an IRC Bouncer, this exists to be an intermediate between an SSH client
and multiple SSH Servers.  
The advantage of connecting this way simplifies identity management, as identity between
individual clients only needs to be maintained between those clients and the "bouncer"
host. All identity management for the upstream SSH servers can be centralized within the
"bouncer" host.

Features:
- Simple, text-based, keyboard driven interface.
- IRC Bouncer style SSH session persitence via GNU Screen.
- Configuration via a basic text file

Planned:
- In-program configuration editing. (Adding and removing connection options, etc)
- Killing or force detaching screen session.

***
# Usage
On start the following menu is displayed:
<pre><samp>Portcullis ===========================================================================
1. Connect
2. List sessions
| b = Back | e = Exit |
======================================================================================
Select menu option:</samp></pre>
Navigation is done by entering the desired letter or number option and presing enter.
Otherwise uses GNU Screen bindings while connected to a session, to detach from a session 
without disconnecting use <kbd><kbd>Ctrl</kbd>+<kbd>a</kbd>+<kbd>d</kbd></kbd>.

***


# Installation
### (Optional) Creating a user
Even in an existing multi-user environment, a separate user is recommended since, when configured as intended, 
you will lose ssh shell access for the user configured. The app also has no user management, and will share 
sessions and connections within the same user.  
Additional notes for creating the account:
- A shell is **REQUIRED** or the script won't be able to run on login, avoid options like
`--system` or `--shell /sbin/nologin`.
- Although a home directory isn't technically needed, if you don't have anywhere for OpenSSH
to read/store configuration, you'll have to accept fingerprints every time, and have no way to specify 
configurations for individual SSH hosts.

## Installing Portcullis
<pre>
# Create a user
<samp>
~ # <kbd>{useradd||adduser} portcullis</kbd>
</samp>

# Clone the repo
<samp>
~ $ <kbd>git clone https://github.com/raku-cat/portcullis.git /opt/portcullis</kbd>

~ $ <kbd>chown -R portcullis:portcullis /opt/portcullis</kbd>
</samp>

# Create the python environment
# If `make` is available on your system, a Makefile is included which should create the
# virtualenv and install the pip requirements
<samp>
~ $ <kbd>cd /opt/portcullis</kbd>
~ $ <kbd>make all</kbd>
</samp>
# Otherwise, if `make` is unavailable
<samp>
~ $ <kbd>python3 -m venv python_modules</kbd>
~ $ <kbd>python_modules/bin/pip install -r requirements.txt</kbd>
</samp>

# Create the config
# Note: An example config is included `servers.list.example`.  
<samp>    
~ $ <kbd>printf "user1@server1.tld
user2@server2.tld
user3@server3.tld" > servers.list</kbd>
</samp>

# Configure OpenSSH
<samp>
~ # <kbd>printf \
"Match User portcullis
    ForceCommand /opt/portcullis/python_modules/bin/python /opt/portcullis/app.py" >> /etc/ssh/sshd_config</kbd>
</samp>   

# Restart sshd
<samp>
~ # <kbd>systemctl restart sshd</kbd>
</samp>
</pre>

## Post installation
Now that the app is set up, manually run it on the Portcullis host to verify functionality:
<pre><samp>~ $ <kbd>/opt/portcullis/python_modules/bin/python /opt/portcullis/app.py</kbd></samp></pre>
