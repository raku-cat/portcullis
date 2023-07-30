<p align="center">
    <img
        src="https://github.com/raku-cat/portcullis/assets/1125449/255651ef-596a-47e9-b4aa-4f76fa836734"
        height="400px"
    />
</p>

<h1 align="center">
    Portcullis
</h1>

<p align="center">
    <i>n.</i> a strong, heavy grating that can be lowered down grooves on each side of a gateway to block it.
</p>

***

<p align="center">
    <img
        src="https://github.com/raku-cat/portcullis/assets/1125449/f5c86125-240c-4139-bdf1-32162b787f62" 
        align="center"
        width="70%"
    />
</p>

***


<h1>About</h1>

Designed after an IRC Bouncer, this project exists to be an intermediate between an SSH client and multiple SSH Servers.
<br>
<h3>Features:</h3>
<ul>
    <li>IRC Bouncer style SSH session persistence via GNU Screen.</li>
    <li>Simple, text-based, keyboard driven interface.</li>
    <li>Configuration uses a basic text file.</li>
    <li>Simplifies access control and identity management with a single entry point for clients;</li>
        <ul>
            <li>All connections to upstream SSH servers are made through the Portcullis host.</li>
            <li>Users/clients only need network access to and maintain identity with the Portcullis host, which itself may have more privileged access.</li>
        </ul>
</ul>
<b>Note:</b> No security is infalliable, a single point of entry is a single point of failure, followbest secuirty practices for your environment.
<br>
<h3>Planned:</h3>
<ul>
    <li>In-program configuration editing. (Adding and removing connection options, etc)</li>
    <li>Additional menus for killing or force detaching screen session.</li>
</ul>


***


<h1>Usage</h1>
On start the following menu is displayed:<br>
<pre><samp>Portcullis  ============================================================================================================================================================
1. Connect
2. List sessions
| b = Back | e = Exit |
======================================================================================================================================================================
Select menu option:</samp></pre>
Navigation is done by entering the desired letter or number option and presing enter.<br>
Otherwise uses GNU Screen bindings while connected to a session, for example, to detach from a session without disconnecting use <kbd><kbd>Ctrl</kbd>+<kbd>a</kbd>+<kbd>d</kbd></kbd>.


***


<h1>Installation</h1>

<h3>(Optional) Creating a user</h3>
Even when running on an existing multi-user host, a separate user is recommended, since, when configured as intended, you will lose ssh shell access for the user configured.<br>
The app also has no user management, and will share sessions and connections within the same user, which may be undesired.<br>
Additional notes for creating the account:<br>
<ul>
    <li>A shell is <b><em>REQUIRED</em></b> or the script won't be able to run on login, avoid options like <samp>--system</samp> or <samp>--shell /sbin/nologin</samp>.</li>
    <li>Although a home directory isn't technically needed, if you don't have anywhere for OpenSSH to read/store configuration, you'll have to accept fingerprints every time, and have no way to specify configurations for individual SSH hosts.</li>
</ul>

<br>

<h2>Installing Portcullis</h2>
<br>

<pre>
# Create a user
<samp>~ # <kbd>{useradd||adduser} portcullis</kbd></samp>
<br>
# Clone the repo
<samp>~ $ <kbd>git clone https://github.com/raku-cat/portcullis.git /opt/portcullis</kbd></samp>
<samp>~ $ <kbd>chown -R portcullis:portcullis /opt/portcullis</kbd></samp>
</samp>
<br>
# Create the python environment
# If `make` is available on your system, a Makefile is included which
# should create the virtualenv and install the pip requirements.
<samp>~ $ <kbd>cd /opt/portcullis</kbd></samp>
<samp>~ $ <kbd>make all</kbd></samp>
# Otherwise, if `make` is unavailable
<samp>~ $ <kbd>python3 -m venv python_modules</kbd></samp>
<samp>~ $ <kbd>python_modules/bin/pip install -r requirements.txt</kbd></samp>
<br>
# Create the config
# Note: An example config is included `servers.list.example`.  
<samp>~ $ <kbd>printf "user1@server1.tld
user2@server2.tld
user3@server3.tld" > servers.list</kbd></samp>
<br>
# Configure OpenSSH
<samp>~ # <kbd>printf \
"Match User portcullis
    ForceCommand /opt/portcullis/python_modules/bin/python /opt/portcullis/app.py" >> /etc/ssh/sshd_config</kbd></samp>
<br>
# Restart sshd
<samp>~ # <kbd>systemctl restart sshd</kbd></samp>
</pre>

<h2>Post installation</h2>
Now that the app is set up, manually run it on the Portcullis host to verify functionality:<br>
<pre><samp>~ $ <kbd>/opt/portcullis/python_modules/bin/python /opt/portcullis/app.py</kbd></samp></pre>
