
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import shutil
from PySide import QtCore

import flickrapi


class FlickrPluginSettings(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

        #fill in your account / app secrets
        self.api_key = ''
        self.api_secret = ''

        self.flickr = flickrapi.FlickrAPI(self.api_key, self.api_secret)

    # Part 1 generates auth link and opens browser with auth url
    # Part 2 is started after authentication via web sited

    @QtCore.Slot()
    def auth_flickr_part1(self):
        print "auth function running"
        (self.token, self.frob) = self.flickr.get_token_part_one(perms='write')

    @QtCore.Slot()
    def auth_flickr_part2(self):
        self.flickr.get_token_part_two((self.token, self.frob))
        self.fake_cfg()

    def fake_cfg(self):
        """
        This function saves an empty cfg file for flickr, because some
        UI elements will be enabled only, if there are a cfg file, but
        flickr don't really need it!
        """

        with open('/home/user/.config/FotoShareN9/fotoshare_flickr_plugin.cfg', "w") as f:
            print "created fake cfg for flickr"


    @QtCore.Slot()
    def unlink_flickr(self):
        """
        Unlinks Flickr by deleting saved token and fake cfg files
        """

        shutil.rmtree('/home/user/.flickr')
        os.remove('/home/user/.config/FotoShareN9/fotoshare_flickr_plugin.cfg')

    @QtCore.Slot(result=str)
    def get_button_text(self):
        """
        Checks the token, and gives back the correct text for QML auth
        button. If the token is okay - Flickr is linked and the
        user maybe want to unlink it, otherwise he wants to link it
        again.
        """

        if not os.path.isdir("/home/user/.flickr"):
            return "Link Flickr"
        else:
            return "Unlink Flickr"
