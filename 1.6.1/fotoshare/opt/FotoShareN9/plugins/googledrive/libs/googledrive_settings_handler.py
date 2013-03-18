
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys

import httplib2

#from apiclient.discovery import build
#from apiclient.http import MediaFileUpload
#from apiclient import errors

from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

from PySide import QtCore


class GoogledrivePluginSettings(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

        # creating json file with secrets from string
        if not os.path.isfile('/home/user/.config/FotoShareN9/client_secrets.json'):
            with open('/home/user/.config/FotoShareN9/client_secrets.json', 'w') as f:

                # FILL IN YOUR ID/SECRET HERE IN THE ""
                json_credentials = """
{
  "web": {
    "client_id": "",
    "client_secret": "",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
"""
                f.write(json_credentials)

        self.cfg_path = '/home/user/.config/FotoShareN9/fotoshare_googledrive_plugin.cfg'
        self.CLIENT_SECRETS = '/home/user/.config/FotoShareN9/client_secrets.json'
        self.MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the APIs Console <https://code.google.com/apis/console>.

""" % os.path.join(os.path.dirname(__file__), self.CLIENT_SECRETS)


    @QtCore.Slot()
    def auth_googledrive(self):
        """
        Check for credentials if they don't exist or invalid create
        new credentials and save them.
        """

        # Set up a Flow object to be used if we need to authenticate.
        FLOW = flow_from_clientsecrets(self.CLIENT_SECRETS,
            scope='https://www.googleapis.com/auth/drive.file',
            message=self.MISSING_CLIENT_SECRETS_MESSAGE)

        # If the Credentials don't exist or are invalid run through the native client
        # flow. The Storage object will ensure that if successful the good
        # Credentials will get written back to a file.
        storage = Storage(self.cfg_path)
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            credentials = run(FLOW, storage)


    @QtCore.Slot()
    def unlink_googledrive(self):
        if os.path.isfile(self.cfg_path):
            print "deleting config"
            os.remove(self.cfg_path)
        else:
            print "no config found - do nothing"


    @QtCore.Slot(result=str)
    def get_button_text(self):
        if os.path.isfile(self.cfg_path):
            return "Unlink GoogleDrive"
        else:
            return "Link GoogleDrive"
