ATTENTION!
==========
The latest version is 1.6.1. Here you'll can get also the older version 0.9.7!
Informations for writing plugins and some details will be added at the wiki in the near future.

If you use the files offered here you have to add the api key and/or other credentials by your own, to get Dropbox, Google Drive ... to work. All standard server related options are working out of the box. 

Also the de_root_script need some modification to fit your user name.

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

Build Information
=================
For 1.6.2 it's just adding acount data/secrets for Dropbox, Google Drive and Flickr (in there libs/<service>_upload_plugin.py files and run the build script. The de_root_script.sh is used to set back the user to the default/non root system user - so change it to fit your system name.

Licence
=======
FotoShareN9 is published under the terms and conditions of the GPL licence version 3.

------------------

Last update: 07.02.2014





