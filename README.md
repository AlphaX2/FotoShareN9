FotoShareN9
===========

FotoShareN9 is an application for the Nokia N9 with MeeGo 1.2 Harmattan. 
It allows the user to push all his shot pictures to Dropbox or a 
selectable server in the moment they are shot.

This is the bunch of features:
==============================
- Upload to Dropbox
- Upload on a server
- use ftp, sftp or scp for uploading
- resize option (in percent) for upload
- startup FotoShareN9 daemon on boot
- Wifi only upload
- optional video upload
- selectable notification types
- instant or interval upload with selectable times
- logfile support
- nice QML GUI

Notes
=====
- If you want upload via SCP and a public key - the public key have to
be named "fotoshare"!

Build Information
=================

Copy fotoshareGUI.py, fotoshare_service and /qml to fotoshare_deb/opt
than open a terminal

At the terminal:
----------------
- cd /your/path/FotoShareN9/src/

- sudo chown -R root:root fotoshare_deb/opt/
- sudo chown -R root:root fotoshare_deb/usr/
- sudo chown -R root:root fotoshare_deb/etc/

- sudo chmod a+x fotoshare_deb/opt/FotoShareN9/fotoshareGUI.py
- sudo chmod a+x fotoshare_deb/opt/FotoShareN9/fotoshare_service

- dpkg-deb -b fotoshare_deb
- ar q fotoshare_deb.deb _aegis

Now you can rename your deb file.

------------------

Last update: 08.06.2012





