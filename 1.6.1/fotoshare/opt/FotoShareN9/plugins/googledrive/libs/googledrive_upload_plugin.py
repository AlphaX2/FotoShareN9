
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import httplib2

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from apiclient import errors

from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run

class GoogledriveUploadPlugin:
    def __init__(self):
        self.cfg_path = '/home/user/.config/FotoShareN9/fotoshare_googledrive_plugin.cfg'

        # CLIENT_SECRETS, name of a file containing the OAuth 2.0 information for this
        # application, including client_id and client_secret, which are found
        # on the API Access tab on the Google APIs
        # Console <http://code.google.com/apis/console>
        self.CLIENT_SECRETS = '/home/user/.config/FotoShareN9/client_secrets.json'

        # Helpful message to display in the browser if the CLIENT_SECRETS file
        # is missing.
        self.MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:

           %s

        with information from the APIs Console <https://code.google.com/apis/console>.

        """ % os.path.join(os.path.dirname(__file__), self.CLIENT_SECRETS)

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

        # Create an httplib2.Http object to handle our HTTP requests and authorize it
        # with our good Credentials.
        http = httplib2.Http()
        http = credentials.authorize(http)

        self.service = build("drive", "v2", http=http)

    def upload(self, data):
        """
        Uploads the file given with the path in 'data'
        """

        print "data am start"
        print data
        print type(data)

        with open(data) as f:
            name = os.path.split(data)
            name = name[-1]

            print "File to upload: "+str(name)

            try:
                title = name
                description = "Photo uploaded with FotoShareN9"
                mime_type = "image/jpeg"
                #parent_id = "0B_xHb9eU7tRvYkxGRU9YZkRlU00"
                filename = data

                media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
                body = {
                    'title': title,
                    'description': description,
                    'mimeType': mime_type
                    #'parents': [{'id': '0B_xHb9eU7tRvYkxGRU9YZkRlU00'}]
                }

                file = self.service.files().insert(body=body, media_body=media_body).execute()
                print 'File ID: %s' % file['id']

                print "GoogleDrive upload finished!"
                print "Success"
                return True

            except:
                print "GoogleDrive upload failed!"
                print "Fail"
                return False

    def test_upload(self):
        """
        Method which could be called to test the upload function
        """

        test_file = "/opt/FotoShareN9/fotoshare_test_file"
        try:
            self.upload(test_file)
            print "GoogleDrive upload works!"
            return True
        except:
            print "GoogleDrive upload failed!"
            return False


if __name__ == "__main__":
    GoogledriveUploadPlugin().test_upload()
