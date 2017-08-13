## Email On Start

Simple systemd service file to use in ubuntu and other linux distributions.
Runs emailstart.py and sends an e-mail using Google smtp server when server/service is started/restarted.

You will need to create a symlink of email_on_start.service in the systemd configuration files:

```
sudo ln -s <repo_dir>/email_on_start.service /etc/systemd/system/.
```

You should also edit that service file to set up the following environment variables:
Environment="EMAIL_USER="
Environment="EMAIL_PASSWD="
Environment="DEST_EMAIL="
Environment="EMAIL_LOG_FILE="

and these flags to use the actual working directory and files:

WorkingDirectory=/home/ria/email-on-start
ExecStart=/usr/bin/python /home/ria/email-on-start/emailstart.py

then, you should enable your service:

```
sudo systemctl enable email_on_start
```

This is not meant to be a terribly reusable script, just thought I'd share. If you need to change he subject or email message contents, you should edit emailstart.py
