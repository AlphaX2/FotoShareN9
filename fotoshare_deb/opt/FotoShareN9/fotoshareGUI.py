#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import re
import ftplib
import pickle
import subprocess

import paramiko
import pexpect
import oauth
import dropbox

from PySide import QtCore
from PySide.QtCore import Qt
from PySide import QtGui
from PySide import QtDeclarative
from PySide import QtOpenGL

class FotoShareN9(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        self.FOTOSHARE_VERSION = "0.9.0-0"

        #Oberfläche und Instanzierungen für QML2Py Funktionen
        self.view = QtDeclarative.QDeclarativeView()

        #OpenGL Rendering
        self.glw = QtOpenGL.QGLWidget()
        self.view.setViewport(self.glw)

        self.view.setSource(QtCore.QUrl('/opt/FotoShareN9/qml/main.qml'))
        self.root = self.view.rootObject()

        #instantiate the Python object
        self.controller = Controller()

        #expose the object to QML
        self.context = self.view.rootContext()
        self.context.setContextProperty('controller', self.controller)

        self.config_path = '/home/user/.config/fotoshare.cfg'

        #loads all important data and settings
        self.preload_settings()

        #Holds pid of daemon, if running, else it's empty.
        self.pid = ''

        #returns the pid of a running daemon to self.pid
        self.getPID()

        print "PID IS: "
        print self.pid

        #set GUI Buttons etc. depending from settings ----------------
        #check for first start
        self.is_first_start()

        #create new settings cfg if version needs new one
        self.check_version()

        #check if daemon boots on startup and set slider on GUI
        self.check_daemon_startup()

        #check resize switch and slider
        self.check_resize_options()

        #check other options from GUI ButtonRows
        self.check_button_options()

        #check that dropbox is linked or not and show on UI
        self.check_dropbox_link()

        #Change menu text in dependency to log status in cfg
        self.check_log_file()

        #holds ssh hostkey
        self.hostkey = None

        #Holds dropbox appkey and app secret for authentification
        self.APP_KEY = 'uvxyouqhkdljbdn'
        self.APP_SECRET = '09sd2chtvifn5aj'
        self.ACCESS_TYPE = 'app_folder'

        #Connections from Controller() class for QML/Py communication
        self.controller.settings_saver.connect(self.save_settings)
        self.controller.settings_loader.connect(self.load_settings)

        self.controller.resize_photos.connect(self.save_resize_option)

        self.controller.notification_select.connect(self.save_notification_type)
        self.controller.save_interval_time.connect(self.save_interval_times) #TIMES not TIME! ;)
        self.controller.video_select.connect(self.select_video_upload)
        self.controller.wifi3g_select.connect(self.select_wifi3g)
        self.controller.upload_type_select.connect(self.select_upload_type)


        #Connections for daemon start/stop and start on boot
        self.controller.daemon.connect(self.start_stop_daemon)
        self.controller.startupDaemon.connect(self.activate_startup_daemon)

        #Test connections and settings set in GUI
        self.controller.contest.connect(self.test_connection)

        #Reset all settings
        self.controller.settings_reset.connect(self.reset_settings)

        #Activate LOG File
        self.controller.activate_log.connect(self.enable_log)

        #Dropbox authentification process stuff
        self.controller.dropbox_authweb_signal.connect(self.get_dropbox_auth_weblink)
        self.controller.dropbox_authsave_signal.connect(self.save_dropbox_auth_token)
        self.controller.dropbox_unlink_signal.connect(self.unlink_dropbox_connection)

# loading and saving settings ----------------------------------------

    def preload_settings(self):
        #Preload all relevant data from settings:
        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            print l

            try:
                self.server_adress = l['server']
                self.server_folder = l['path'] 
                self.server_user = l['username']
                self.server_pass = l['pass']
                self.server_port = l['port']
                self.connection_type = l['connection']
                self.connection_radio = l['data_connection']
                self.upload_type = l['upload_type']
                self.daemon_startup = l['daemon_startup']
                self.db_sync_status = l['db_sync']
                self.access_token = l['db_access_token']
                self.access_secret = l['db_access_secret']
                self.video_upload = l['video_upload']
                self.interval_time = l['interval_time']
                self.version = l['version']
                self.log = l['log']
                self.resize = l['resize']
                self.notification_type = l['notification_type']
            except:
                self.version = None

            print "self version is:"
            print self.version

        else:
            self.server_adress = ''
            self.server_folder = ''
            self.server_user = ''
            self.server_pass = ''
            self.server_port = ''
            self.connection_type = ''
            self.connection_radio = '3G'
            self.upload_type = 'instant'
            self.daemon_startup = ''
            self.db_sync_status = 'False'
            self.access_token = ''
            self.access_secret = ''
            self.video_upload = 'forbidden'
            self.interval_time = 5
            self.version = self.FOTOSHARE_VERSION
            self.log = 'no'
            self.notification_type = 'off'
            self.resize = 0


            print "self version is = FOTOSHARE_VERSION"
            print self.version

    def is_first_start(self):
        """
        check for first start - set switch in QML UI
        """

        #if os.path.isfile(self.config_path):
        if self.server_adress == '' and self.db_sync_status == 'False':
            print "First start"
            #self.first_start = False
            self.root.switchON('false')
        else:
            print "Not first start"
            #self.first_start = True
            self.root.switchON('true')

    def check_version(self):
        """
        Check the version of cfg and creates a new one, if no version
        key can be found, or a new FotoShareN9 version is detected.
        """

        if self.version == None:
            print "No version controll found: create new cfg"
            self.reset_settings()
            self.root.switchON('false')
            self.start_stop_daemon() #stop if running
        else:
            if not self.version == self.FOTOSHARE_VERSION:
                print "New version of FotoShareN9: reset and create new cfg."
                self.reset_settings()
                self.root.switchON('false')
                self.start_stop_daemon() #stop if running

    def check_daemon_startup(self):
        """
        If daemon is allowed to start on boot set slider on UI to show it
        """

        print "daemon_startup: "
        print self.daemon_startup

        if self.daemon_startup == 'yes':
            print "check startup slider: true"
            self.root.switchDaemonCHECK()

    def check_resize_options(self):
        """
        Check if resize is active and set slider
        """
        if self.resize > 0:
            print "resize erkannt"
            self.root.switchResizeCHECK(self.resize)


    def check_button_options(self):
        """
        Checks selected options from ButtonRows on MainPage and set UI
        """

        #TODO: upload only / sync mode option

        if self.notification_type != 'off':
            print "Notify type is:"
            print self.notification_type
            self.root.notificationTypeButtonCHECKED(self.notification_type)

        #check for instant/interval upload
        if self.upload_type == 'interval':
            self.root.intervalUploadCHECKED(str(self.interval_time))

        #check if videoupload is allowed
        if self.video_upload == 'allowed':
            self.root.videoUploadButtonCHECKED()

        #check wifi only upload and set button
        if self.connection_radio == u'Wlan':
            self.root.wifiButtonCHECKED()

        #check for server settings and enable option buttons or not
        if not self.server_adress == '' or not self.db_sync_status == 'False':

            self.root.switchDaemonONOFF()
            self.root.switchResizeONOFF()

            self.root.wifi3GButtonENABLED()
            self.root.uploadTypeButtonENABLED()
            self.root.videoUploadButtonENABLED()
            self.root.notificationTypeButtonENABLED()

    def check_log_file(self):
        if self.log == 'yes':
            self.root.updateLogText('yes')
        else:
            self.root.updateLogText('no')


    def check_dropbox_link(self):
        """
        check if Dropbox is linked or not and show on UI button
        second arg is for Dropbox auth url, but not passed here.
        """

        if self.access_token == '' and self.access_secret == '':
            print "not linked"
            self.root.update_dropbox_auth_button('Link Dropbox', '')
        else:
            print "linked"
            self.root.update_dropbox_auth_button('Unlink Dropbox', '')

    def load_settings(self):
        """
        Loads saved settings and show them in the QML UI.
        """
        print "Load settings"
        self.root.updateSettingsText(self.server_adress,
                                     self.server_folder,
                                     self.server_user,
                                     self.server_pass,
                                     self.connection_type,
                                     self.server_port
                                     )
        print "Load ended."


    def save_settings(self, server, path, user, passw, connect, port):
        """
        Saves settings, which are set in the QML UI SettingsPage
        """

        #path should be without root "/" so terminate it here
        if path.startswith('/'):
            path = path[1:]

        #If not a server is selected changes connection type to "" for
        #preventing errors.
        if not server:
            connect = ''

        #update arguments for running app/window class
        self.server_adress = str(server)
        self.server_folder = str(path)
        self.server_user = str(user)
        self.server_pass = str(passw)
        self.connection_type = str(connect)
        self.server_port = str(port)

        #load config file or create a new one
        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)
        else:
            f = open(self.config_path, 'w')
            pickle.dump(
                        {
                         'server':'',
                         'port':'',
                         'path':'',
                         'username':'',
                         'pass':'',
                         'connection':'',
                         'data_connection': '3G',
                         'daemon_startup': '',
                         'video_upload': 'forbidden',
                         'interval_time': 5,
                         'upload_type': 'instant',
                         'db_sync': 'False',
                         'db_access_token': '',
                         'db_access_secret': '',
                         'version': self.FOTOSHARE_VERSION,
                         'log': 'no',
                         'resize': 0,
                         'notification_type':'off'
                         }, f)

            f = open(self.config_path)
            l = pickle.load(f)

        l['server'] = str(server)
        l['port'] = str(port)
        l['path'] = str(path)
        l['username'] = str(user)
        l['pass'] = str(passw)
        l['connection'] = str(connect)

        #save config
        f = open(self.config_path, 'w')
        pickle.dump(l,f)
        f.close()


    def save_interval_times(self, time):
        """
        Saves the selected interval time
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['interval_time'] = int(time)
            print "Interval upload time is now: "+str(time)+" Minutes."

            #save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def save_notification_type(self, typus):
        """
        Saves the selected notification type
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['notification_type'] = str(typus)
            print "Notification type is now: "+str(typus)

            #save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def enable_log(self):
        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            if l['log'] == 'yes':
                l['log'] = 'no'
            else:
                l['log'] = 'yes'

            self.log = l['log']
            self.root.updateLogText(str(self.log))

            print "Is log active? "+str(self.log)

            #save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def reset_settings(self):
        """
        Deletes all configuration data and loads default.

        It will be called if user selected reset on the GUI and if a 
        new version of FotoShareN9 is started, which has more or less 
        options than the older version. So the user have to set 
        everything again, but don't have to delete it's cfg and sav 
        file by hand.

        After reset, preload_settings function create a new cfg and
        loads default settings.
        """

        if os.path.isfile(self.config_path):
            os.remove(self.config_path)
            self.preload_settings()
        else:
            print "No reset is done, because no cfg file was found."

        if os.path.isfile("/home/user/.config/fotoshare_offline.sav"):
            os.remove("/home/user/.config/fotoshare_offline.sav")
        else:
            print "No _offline.sav found - do nothing."


    def save_resize_option(self, percent):
        print "resize function"
        """
        Saves the selected resize option
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['resize'] = percent
            self.resize = percent

            print "Resize is now: "+str(self.resize)+" %"

            #save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


    def select_sync_type(self, sync):
        """
        Saves the setting from GUI: 'Upload only' vs. 'Sync'
        """
        pass

    def select_video_upload(self, typus):
        """
        Saves setting from GUI: 'No video upload' vs. 'Video upload'
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['video_upload'] = typus
            print "Video upload is now: "+str(typus)

            #save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()

    def select_upload_type(self, typus):
        """
        Saves setting from GUI: 'Instant sync' vs. 'Inverval sync'
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['upload_type'] = typus
            print "Upload type is now: "+str(typus)

            #save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()

    def select_wifi3g(self, radio):
        """
        Saves setting from GUI: 'Wifi only' vs. 'Wifi and 3G'
        """

        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)

            l['data_connection'] = radio
            print "Upload is now: "+str(radio)

            #save config
            f = open(self.config_path, 'w')
            pickle.dump(l,f)
            f.close()


#main functions ------------------------------------------------------

    def getPID(self):
        """
        Parses the pid of the fotoshare_service daemon and set the
        number to self.pid, also updates daemon on startup switch
        in the QML UI MainPage.
        """

        cmd = 'ps aux|grep python'
        pid = os.popen(cmd)
        data = pid.readlines()

        print data

        for i in data:
            if 'fotoshare_service' in i:
                daemon_pid = re.findall(r'\b\d+\b', str(i))
                self.pid = daemon_pid[0]
                self.root.switchCHECKED('true')
                print 'Daemons pid is: '+daemon_pid[0]

    def get_hostkey(self, hostname):
        """
        Reads server hostkeys from ~/.ssh/known_hosts and sets self.hostkey
        """

        hostkeytype = None
        hostkey = None

        try:
            host_keys = paramiko.util.load_host_keys(
                             os.path.expanduser('~/.ssh/known_hosts'))
        except IOError:
            try:
                #try ~/ssh/ too, because windows can't have a folder named ~/.ssh/
                host_keys = paramiko.util.load_host_keys(
                              os.path.expanduser('~/ssh/known_hosts'))
            except IOError:
                print '*** Unable to open host keys file'
                host_keys = {}

        if host_keys.has_key(hostname):
            hostkeytype = host_keys[hostname].keys()[0]
            self.hostkey = host_keys[hostname][hostkeytype]
            print 'Using host key of type %s' % hostkeytype


    def start_stop_daemon(self):
        """
        Starts and stops daemon from QML UI
        """

        if self.pid == '':
            print 'Daemon is not running and will start now!'
            subprocess.Popen(['/opt/FotoShareN9/fotoshare_service','&'])
            self.getPID()
        else:
            print 'Daemon was running and its PID was: '+str(self.pid)
            subprocess.Popen(['kill', '%d' %(int(self.pid))])
            self.pid = ''
            self.root.switchCHECKED('false')


    def activate_startup_daemon(self):
        """
        QML UI option (Switch) about starting daemon on boot or not.

        Sets an entry in fotoshare.cfg (yes/no) which holds the info
        about the daemon is allowed to run from boot or not. It is
        also read by the daemon on startup, if set to "no" the daemon
        stops, otherwise stays on.
        """

        print "activate_startup_daemon"

        if os.path.isfile(self.config_path):
            #Laden der gespeicherten Werte
            f = open(self.config_path)
            l = pickle.load(f)

            daemon = l['daemon_startup']
            print daemon

            #'yes' and 'no' is used, because True/False didn't work.
            if daemon == 'yes':
                status = ''
            if daemon == '':
                status = 'yes'

            print status

            l['daemon_startup'] = status

        #Save data
        f = open(self.config_path, 'w')
        pickle.dump(l,f)
        f.close()

#Dropbox Handling-----------------------------------------------------

    def get_dropbox_auth_weblink(self):
        """
        Generates an authentication weblink for Dropbox and shows a
        link on the GUI.
        """

        #if user want to authenticate
        print "Dropbox auth"
        self.drop_session = dropbox.session.DropboxSession(self.APP_KEY,
                                                           self.APP_SECRET,
                                                           self.ACCESS_TYPE)
        self.request_token = self.drop_session.obtain_request_token()
        url = self.drop_session.build_authorize_url(self.request_token)
        #URL is only passed here to GUI
        self.root.update_dropbox_auth_button("Ok", url)

    def save_dropbox_auth_token(self):
        """
        Generates an access token from request token and saves them.
        """

        print "Dropbox save"
        # This will fail if the user didn't visit the Auth-URL and hit 'Allow'
        self.access_token = self.drop_session.obtain_access_token(self.request_token)
        self.save_dropbox_settings(self.access_token.key, self.access_token.secret)
        self.root.update_dropbox_auth_button('Unlink Dropbox', "")

    def unlink_dropbox_connection(self):
        """
        Destroys the link to Dropbox and reset settings.
        """

        print "Dropbox unlink"
        #If user want to destroy the connection from app to dropbox
        self.drop_session = None
        self.save_dropbox_settings('', '')
        self.root.update_dropbox_auth_button('Link Dropbox', '')

    def save_dropbox_settings(self, access_token, access_secret):
        """
        Saves Dropbox access token informations from authentification.
        """

        #load config file or create a new one
        if os.path.isfile(self.config_path):
            f = open(self.config_path)
            l = pickle.load(f)
        else:
            f = open(self.config_path, 'w')
            pickle.dump(
                        {
                         'server':'',
                         'port':'',
                         'path':'',
                         'username':'',
                         'pass':'',
                         'data_connection': '3G',
                         'connection':'',
                         'daemon_startup': '',
                         'upload_type': 'instant',
                         'video_upload': 'forbidden',
                         'interval_time': 5,
                         'db_sync': 'False',
                         'db_access_token': '',
                         'db_access_secret': '',
                         'version': self.FOTOSHARE_VERSION,
                         'log': 'no',
                         'notification_type':'off',
                         'resize': 0,
                         }, f)

            f = open(self.config_path)
            l = pickle.load(f)

        l['db_access_token'] = str(access_token)
        l['db_access_secret'] = str(access_secret)

        #Update them to be sure the open app has the newest informations.
        self.access_token = str(access_token)
        self.access_secret = str(access_secret)

        #db_sync_status allows to sync only DB or DB+webserver!
        if self.access_token == '' and self.access_secret == '':
            l['db_sync'] = 'False'
            self.db_sync_status = 'False'
            print self.db_sync_status
        else:
            l['db_sync'] = 'True'
            self.db_sync_status = 'True'
            print self.db_sync_status

        #save config
        f = open(self.config_path, 'w')
        pickle.dump(l,f)
        f.close()

# Connection testing -------------------------------------------------

    def test_connection(self, con_type):
        """
        Function tests the settings and connection type set on the UI
        """

        #load server settings
        print 'Connection type is: '+con_type
        print self.server_adress
        print self.server_folder
        print self.server_user
        print self.server_pass
        print self.connection_type
        print self.server_port

        #Try to connect via ftp TODO: add port to ftp-login
        if con_type == 'ftp':
            print 'Testing ftp'
            try: 
                self.ftp = ftplib.FTP()#self.server_adress)
                self.ftp.connect(self.server_adress, self.server_port)
                self.ftp.getwelcome()
                self.root.callConnectionDialog('ok')
            except:
                self.root.callConnectionDialog('fail')

        #Try to connect via sftp
        if con_type == 'sftp':
            'Testing sftp'
            self.get_hostkey(self.server_adress)
            try:
                t = paramiko.Transport((self.server_adress, 
                                        int(self.server_port)))

                t.connect(username=self.server_user,
                          password=self.server_pass,
                          hostkey=self.hostkey)

                sftp = paramiko.SFTPClient.from_transport(t)
                sftp.chdir(self.server_folder)
                t.close()
                self.root.callConnectionDialog('ok')
            except:
                self.root.callConnectionDialog('fail')

        #Try to connect via scp
        if con_type == 'scp':
            print 'Testing scp'

            test = '/opt/FotoShareN9/scp_test_file'
            dest = self.server_user+'@'+self.server_adress+':/'+self.server_folder

            self.get_hostkey(self.server_adress)

            #get number of files at .ssh for checking "fotoshare" key is in it
            files_at_ssh = os.listdir('/home/user/.ssh')

            if not os.path.isdir('/home/user/.ssh'):
                print "scp: no ~/.shh found"
                try:
                    scp = pexpect.spawn('scp %r %r' %(test, dest))
                    scp.expect("Are you sure you want to continue connecting (yes/no)?")
                    scp.sendline("yes")
                    scp.expect(self.server_user+'@'+self.server_adress+"'s password:")
                    scp.sendline(self.server_pass)
                    scp.wait()
                    self.root.callConnectionDialog('ok')

                except:
                    print "SCP: except @ no .ssh dir"
                    self.root.callConnectionDialog('fail')

            if self.hostkey and not 'fotoshare' in files_at_ssh:
                print "scp: no publickey found"
                try:
                    scp = pexpect.spawn('scp %r %r' %(test, dest))
                    scp.expect(self.server_user+'@'+self.server_adress+"'s password:")
                    scp.sendline(self.server_pass)
                    scp.wait()
                    self.root.callConnectionDialog('ok')
                except:
                    print "SCP: except @ known_hosts only"
                    self.root.callConnectionDialog('fail')

            if self.hostkey and 'fotoshare' in files_at_ssh:
                print "scp: publickey found"
                try:
                    scp = pexpect.spawn('scp %r %r' %(test, dest))
                    #FotoShareN9 accept only a public key with the name "fotoshare"
                    scp.expect("Enter passphrase for key '/home/user/.ssh/fotoshare: ")
                    scp.sendline(self.server_pass)
                    scp.wait()
                    self.root.callConnectionDialog('ok')
                except:
                    print "SCP: except @ public key auth"
                    self.root.callConnectionDialog('fail')


        #Try to connect via Dropbox
        if self.db_sync_status == 'True':
            print 'testing dropbox'
            try:
                session = dropbox.session.DropboxSession(self.APP_KEY, self.APP_SECRET, self.ACCESS_TYPE)
                session.set_token(self.access_token, self.access_secret)
                client = dropbox.client.DropboxClient(session)
                print client.account_info()
                self.root.callConnectionDialog('ok')
            except:
                self.root.callConnectionDialog('fail')

#Controller Class for QML to Python communication---------------------

class Controller(QtCore.QObject):
    """
    Controller class is connected to QML and receives signals, which
    are send from QML and connects them to Python functions.
    """
    dropbox_authweb_signal = QtCore.Signal()
    dropbox_authsave_signal = QtCore.Signal()
    dropbox_unlink_signal = QtCore.Signal()

    settings_saver = QtCore.Signal(str, str, str, str, str, str)
    settings_loader = QtCore.Signal()
    save_interval_time = QtCore.Signal(str)
    upload_type_select = QtCore.Signal(str)
    wifi3g_select = QtCore.Signal(str)
    video_select = QtCore.Signal(str)
    notification_select = QtCore.Signal(str)
    resize_photos = QtCore.Signal(int)

    activate_log = QtCore.Signal()
    daemon = QtCore.Signal()
    startupDaemon = QtCore.Signal()

    #connection test
    contest = QtCore.Signal(str)

    settings_reset = QtCore.Signal()

    def __init__(self):
        QtCore.QObject.__init__(self)

    @QtCore.Slot(str)
    def auth_dropbox_signal(self, status):
        if status == "web":
            self.dropbox_authweb_signal.emit()
        if status == "save":
            self.dropbox_authsave_signal.emit()
        if status == "unlink":
            self.dropbox_unlink_signal.emit()

    @QtCore.Slot(str, str, str, str, str, str)
    def save_settings_signal(self, server, path, user, passw, connect, port):
        self.settings_saver.emit(server, path, user, passw, connect, port)

    @QtCore.Slot()
    def load_settings_signal(self):
        self.settings_loader.emit()

    @QtCore.Slot(str)
    def save_interval_time_signal(self, time):
        self.save_interval_time.emit(time)

    @QtCore.Slot(str)
    def upload_type_select_signal(self, typus):
        self.upload_type_select.emit(typus)

    @QtCore.Slot(str)
    def wifi3g_select_signal(self, radio):
        self.wifi3g_select.emit(radio)

    @QtCore.Slot(str)
    def video_select_signal(self, typus):
        self.video_select.emit(typus)

    @QtCore.Slot()
    def start_daemon_signal(self):
        self.daemon.emit()

    @QtCore.Slot(str)
    def test_connection_signal(self, con_type):
        self.contest.emit(con_type)

    @QtCore.Slot()
    def activate_startup_daemon_signal(self):
        self.startupDaemon.emit()

    @QtCore.Slot()
    def settings_reset_signal(self):
        self.settings_reset.emit()

    @QtCore.Slot()
    def enable_log_file_signal(self):
        self.activate_log.emit()

    @QtCore.Slot(str)
    def notification_select_signal(self, typus):
        self.notification_select.emit(typus)

    @QtCore.Slot(int)
    def resize_photos_signal(self, percent):
        self.resize_photos.emit(percent)

#Starting the app ----------------------------------------------------
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    start = FotoShareN9()
    start.view.showFullScreen()
    sys.exit(app.exec_())
