<h1 align="center">
    Portcullis - An SSH "bouncer" written in Python
</h1>

<img 
    src="https://github.com/raku-cat/portcullis/assets/1125449/f5c86125-240c-4139-bdf1-32162b787f62" 
    align="right" 
    height="500"
/>

### Portcullis
*n.* a strong, heavy grating that can be lowered down grooves on each side of a gateway to block it.


<img
  src="https://github.com/raku-cat/portcullis/assets/1125449/255651ef-596a-47e9-b4aa-4f76fa836734"
  align="left"
  height="350"
/>

<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>

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
```
Portcullis ===========================================================================
1. Connect
2. List sessions
| b = Back | e = Exit |
======================================================================================
Select menu option:
```
Navigating is done by entering the desired letter or number option and presing enter.

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
```
# Create a user
~ # {useradd||adduser} portcullis

# Clone the repo
~ $ git clone https://github.com/raku-cat/portcullis.git /opt/portcullis

~ $ chown -R portcullis:portcullis /opt/portcullis

# Create the python environment
# If `make` is available on your system, a Makefile is included which should create the
# virtualenv and install the pip requirements
~ $ cd /opt/portcullis
~ $ make all
# Otherwise, if `make` is unavailable
~ $ python3 -m venv python_modules
~ $ python_modules/bin/pip install -r requirements.txt

# Create the config
# Note: An example config is included `servers.list.example`.  
~ $ printf "user1@server1.tld
user2@server2.tld
user3@server3.tld" > servers.list

# Configure OpenSSH
~ # printf \
"Match User portcullis
    ForceCommand /opt/portcullis/python_modules/bin/python /opt/portcullis/app.py" >> /etc/ssh/sshd_config

# Restart sshd
~ # systemctl restart sshd
```

## Post installation
Now that the app is set up, manually run it on the Portcullis host to verify functionality:
```
~ $ /opt/portcullis/python_modules/bin/python /opt/portcullis/app.py
```
