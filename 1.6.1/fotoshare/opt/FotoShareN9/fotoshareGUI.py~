#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import re
import time
import ftplib
import pickle
import subprocess

from PySide import QtCore
from PySide.QtCore import Qt
from PySide import QtGui
from PySide import QtDeclarative
from PySide import QtOpenGL
from PySide.QtNetwork import QNetworkConfigurationManager, QNetworkConfiguration


__fotoshare_version__ = '0.9.7'
__config_path__ = '/home/user/.config/FotoShareN9/fotoshare.cfg'
__plugin_path__ = '/opt/FotoShareN9/plugins/'


class QmlWindow(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)
        # OpenGL Rendering
        glw = QtOpenGL.QGLWidget()

        self.view = QtDeclarative.QDeclarativeView()
        self.view.setViewport(glw)

        # expose the object to QML
        self.context = self.view.rootContext()
        self.context.setContextProperty('main', main)
        self.context.setContextProperty('config', config)
        self.context.setContextProperty('plugin', plugin)

        self.view.setSource(QtCore.QUrl('/opt/FotoShareN9/qml/main.qml'))
        # NOTE: used for services listview delegation via JavaScript,
        # connection test result and en/disable text for log in menu
        self.root = self.view.rootObject()
        self.view.showFullScreen()




class Config(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)

        self.load_settings()
        self.pid = None
        self.check_pid()


    def load_settings(self):
        """
        Loading settings from cfg if possible, or load default settings.

        If it was not able to load settings something went wrong, or 
        there is just no file: load default settings. Also version
        of last FotoShareN9 version is loaded and will later be checked
        that there is no newer one - if so create new cfg.
        """

        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            print "-------------- Found settings file ---------------"
            print
            print "These are the settings:"
            print
            print l
            print

            try:
                self.connection_types = l['connection_types']
                self.connection_radio = l['connection_radio']
                self.upload_type = l['upload_type']
                self.daemon_startup = l['daemon_startup']
                self.video_upload = l['video_upload']
                self.interval_time = l['interval_time']
                self.version = l['version']
                self.log = l['log']
                self.resize_option = l['resize_option']
                self.resize_scale = l['resize_scale']
                self.notification_type = l['notification_type']
            except:
                self.version = None

        else:
            self.create_settings()


    def create_settings(self):
        """
        Creates a settings config file if there isn't a file.
        """

        if os.path.isfile(__config_path__):
            pass

        else:
            print "-------------- Creating a settings file --------------"
            print "processing..."

            with open(__config_path__, 'w') as f:
                pickle.dump(
                            {
                             'connection_types': [],
                             'connection_radio': '3G',
                             'daemon_startup': '',
                             'video_upload': 'forbidden',
                             'interval_time': 5,
                             'upload_type': 'instant',
                             'version': __fotoshare_version__,
                             'log': 'no',
                             'resize_option': 'no',
                             'resize_scale' : 0,
                             'notification_type':'off'
                              }, f)

            print "created successfully a new settings file!"

        self.load_settings()

# Gui related checks -------------------------------------------------

    def check_pid(self):
        """
        Parses the pid of the fotoshare_service daemon and set the
        number to self.pid. Also updates switch in the GUI if it is
        running on app start.
        """

        cmd = 'ps aux | grep python'
        pid = os.popen(cmd)
        data = pid.readlines()

        # Set to true if a running daemon was found, if not it's false
        # and an indicator that self.pid have to be set/stay None
        status = False

        print "THIS IS DATA!"
        print data

        for i in data:
            if 'fotoshare_service' in i:
                daemon_pid = re.findall(r'\b\d+\b', str(i))
                status = True
                print "running daemon found"
                print "pid is: "+daemon_pid[0]
                self.pid = daemon_pid[0]

        if status == False:
            self.pid = None


    def check_version(self):
        """
        Check the version of cfg and creates a new one if no version
        key can be found, or a new FotoShareN9 version is detected.
        If there is a newer version detected, it will reset all data
        to be sure that a new and working config is generated!
        """

        if self.version == None:
            print "No version control found: create new cfg"
            self.reset_settings()
            self.start_stop_daemon() # stop daemon if running
        else:
            if not self.version == self.FOTOSHARE_VERSION:
                print "New FotoShareN9 version: reset and create new cfg."
                self.reset_settings()
                self.start_stop_daemon() # stop daemon if running


    @QtCore.Slot(result=bool)
    def check_not_first_start(self):
        """
        check for first start - enable MainPage UI elements

        one active plugin is enough
        """

        print "check_not_first_start() is running, these are the plugins:"
        active_plugins = os.listdir('/home/user/.config/FotoShareN9')
        is_cfg = False

        #no plugin.cfg means no settings means everything is greyed out
        for i in active_plugins:
            if '_plugin.cfg' in i:
                is_cfg = True

        return is_cfg



    @QtCore.Slot(result=bool)
    def check_daemon_running(self):
        """
        Checks the daemon is running or not
        """

        print "check_daemon_running()"

        if not self.pid:
            return False
        else:
            return True


    @QtCore.Slot(result=bool)
    def check_daemon_startup(self):
        """
        If daemon is allowed to start on boot set slider on UI to show it.
        """

        print "check_daemon_startup()"
        return self.daemon_startup == 'yes'


    @QtCore.Slot(result=bool)
    def check_resize_option(self):
        """
        Check if resize is active and set slider on GUI to show it.
        """

        print "check_resize_option()"
        return self.resize_option == 'yes'


    @QtCore.Slot(result=int)
    def check_resize_percent(self):

        print "check_resize_percent()"
        return self.resize_scale


    @QtCore.Slot(result=unicode)
    def check_notification_type_button(self):
        """
        Sets selected options for Notfication ButtonRow element
        """

        if self.notification_type != 'off':
            print "Notification is:"+str(self.notification_type)
            return self.notification_type
        else:
            print "Notification is off"
            return 'off'


    @QtCore.Slot(result=bool)
    def check_upload_type_button(self):
        """
        Returns upload type instant/interval
        """
        return self.upload_type == 'interval'


    @QtCore.Slot(result=int)
    def check_interval_time(self):
        """
        Returns selected interval time
        """
        return self.interval_time


    @QtCore.Slot(result=bool)
    def check_video_upload_button(self):
        """
        Returns video upload is allowed or not
        """
        return self.video_upload == 'allowed'


    @QtCore.Slot(result=bool)
    def check_connection_type_button(self):
        """
        Returns if "wifi only" is checked or not
        """
        return self.connection_radio == "Wlan"


    @QtCore.Slot(result=bool)
    def check_log_file_enabled(self):
        """
        Set log file text in menu depending on the fact it is on/off
        """
        return self.log == 'yes'


# main functions -----------------------------------------------------

class FotoShareN9(QtCore.QObject):
    def __init__(self):
        QtCore.QObject.__init__(self)


    @QtCore.Slot(result=str)
    def load_services(self):
        """
        Reads plugins from plugins/settings and creates a listview of
        all services on the UI also it gives the path to the services
        QML settings page to the ListModel
        """

        # read available plugins from plugins/settings
        plugins = []

        for i in os.listdir(__plugin_path__):
            if os.path.isfile(__plugin_path__+i):
                plugins.append(i)

        print plugins

        # service list holds Name, Info and QML path of the plugin
        service_list = []

        for service in plugins:
            with open(__plugin_path__+service) as f:
                f = f.readlines()
                for line in f:
                    line = line.replace('\n', '')
                    service_list.append(line)

        print service_list

        window.root.create_services_listview(service_list)


    @QtCore.Slot(str)
    def save_connections(self, name):
        """
        Save selected connections from SettingsPage
        """

        # Check for the name and add it if missing or delete if allready there
        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            type_list = l['connection_types']

            if name in type_list:
                type_list.remove(name)
            else:
                type_list.append(name)

            with open(__config_path__, 'w') as f:
                pickle.dump(l,f)


    @QtCore.Slot()
    def save_resize_option(self):
        """
        Saves the selected resize option
        """

        print "resize option runs"

        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            if l['resize_option'] == 'yes':
                l['resize_option'] = 'no'
            else:
                l['resize_option'] = 'yes'

            print "Resize is now: "+str(l['resize_option'])

            # save config
            with open(__config_path__, 'w') as f:
                pickle.dump(l,f)


    @QtCore.Slot(int)
    def save_resize_scale(self, percent):
        """
        Saves the selected resize scale in percent
        """

        print "RESIZE SCALE LÄUFT"

        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            l['resize_scale'] = percent

            print "Resize is now: "+str(percent)+" %"

            # save config
            with open(__config_path__, 'w') as f:
                pickle.dump(l,f)


    @QtCore.Slot(str)
    def save_notification_type(self, typus):
        """
        Saves the selected notification type
        """

        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            l['notification_type'] = str(typus)
            print "Notification type is now: "+str(typus)

            # save config
            with open(__config_path__, 'w') as f:
                pickle.dump(l,f)


    @QtCore.Slot(str)
    def save_video_upload_option(self, typus):
        """
        Saves setting from GUI: 'No video upload' vs. 'Video upload'
        """

        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            l['video_upload'] = typus
            print "Video upload is now: "+str(typus)

            # save config
            with open(__config_path__, 'w') as f:
                pickle.dump(l,f)


    @QtCore.Slot(str)
    def save_wifi3g_option(self, radio):
        """
        Saves setting from GUI: 'Wifi only' vs. 'Wifi and 3G'
        """

        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            l['connection_radio'] = radio
            print "Upload is now: "+str(radio)

            # save config
            with open(__config_path__, 'w') as f:
                pickle.dump(l,f)


    @QtCore.Slot(str)
    def save_upload_type(self, typus):
        """
        Saves setting from GUI: 'Instant sync' vs. 'Inverval sync'
        """

        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            l['upload_type'] = typus
            print "Upload type is now: "+str(typus)

            with open(__config_path__, 'w') as f:
                pickle.dump(l,f)


    @QtCore.Slot(str)
    def save_interval_time(self, time):
        """
        Saves the selected interval time
        """

        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            l['interval_time'] = int(time)
            print "Interval upload time is now: "+str(time)+" Minutes."

            # save config
            with open(__config_path__, 'w') as f:
                pickle.dump(l,f)


    @QtCore.Slot()
    def enable_log(self):
        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            if l['log'] == 'yes':
                l['log'] = 'no'
            else:
                l['log'] = 'yes'

            log = l['log']
            window.root.updateLogText(str(log))

            print "Is log active? "+str(log)

            # save config
            with open(__config_path__, 'w') as f:
                pickle.dump(l,f)


    @QtCore.Slot()
    def reset_settings(self):
        """
        Deletes all configuration data and loads default.

        It will be called if user selected reset on the GUI and if a 
        new version of FotoShareN9 is started, which has more or less 
        options than the older version. So the user have to set 
        everything again, but don't have to delete it's cfg and sav 
        files by hand.

        After reset, preload_settings function create a new cfg and
        loads default settings.
        """

        if os.path.isfile(__config_path__):
            #remove standard FotoShareN9 config
            os.remove(__config_path__)

            #remove plugin configs
            files = os.listdir('/home/user/.config/FotoShareN9')
            for cfg in files:
                if '_plugin.cfg' in cfg:
                    print cfg
                    os.remove('/home/user/.config/FotoShareN9/'+cfg)

            #Stops FotoShareN9 after deleting all settings
            sys.exit(0)


    @QtCore.Slot()
    def start_stop_daemon(self):
        """
        Starts and stops daemon from QML UI
        """

        print "START STOP DAEMON RUNS"

        if config.pid:
            print "Daemon IS running and will be STOPPED now!"
            subprocess.Popen(['kill', config.pid])
            # wait, to be sure that daemon is killed properly
            time.sleep(1)
            config.check_pid()

        else:
            print "Daemon is NOT running and will be STARTED now!"
            subprocess.Popen(['/opt/FotoShareN9/fotoshare_service', '&'])
            config.check_pid()

        print "The daemon pid is now: "
        print config.pid


    @QtCore.Slot()
    def activate_startup_daemon(self):
        """
        Python logic of QML Switch for starting daemon on boot or not.

        Sets an entry in fotoshare.cfg (yes/no) which holds the info
        about the daemon is allowed to run from boot or not. It will
        also be read by the daemon on startup, if set to "no" the daemon
        stops, otherwise stays on.
        """

        print "ACTIVATE STARTUP DAEMON LÄUFT"

        if os.path.isfile(__config_path__):
            # Laden der gespeicherten Werte
            with open(__config_path__) as f:
                l = pickle.load(f)

            daemon = l['daemon_startup']
            print daemon

            # 'yes' and 'no' is used, because True/False didn't work.
            if daemon == 'yes':
                status = ''
            if daemon == '':
                status = 'yes'

            print "Daemon startup is set to: "+status

            l['daemon_startup'] = status

            # Save data
            with open(__config_path__, 'w') as f:
                pickle.dump(l,f)


class PluginHandler(QtCore.QObject):
    """
    Class that handles plugins
    """

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.plugin_name = None

    @QtCore.Slot(str)
    def register_plugin(self, name):
        self.plugin_name = name
        self.import_name = name+"_settings_handler"
        self.as_name = name+"_settings"
        self.instance_name = name.title()+"PluginSettings"
        self.qml_binding_name = name+"_plugin"
        self.instance = "self.instance"

    @QtCore.Slot()
    def load_plugin(self):
        #extend the path, where Python search libs, to the plugin libs
        lib_path = __plugin_path__+self.plugin_name+'/libs'
        sys.path.append(lib_path)

        # NOTE:
        # The final import statement looks like this:
        # import dropbox_settings_handler as dropbox_settings

        load_plugin_string = 'import '+self.import_name+" as "+self.as_name
        print "load_plugin_string is:"
        print load_plugin_string

        create_binding_string = self.instance+" = "+self.as_name+"."\
+self.instance_name+"()"

        # execute plugin import
        exec load_plugin_string

        # execute the class binding
        exec create_binding_string

        # 'window' is main instance of FotoShareN9() class, where we 
        # want to bind the plugin to!
        print self.qml_binding_name
        window.context.setContextProperty(str(self.qml_binding_name),
                                                        self.instance)


    @QtCore.Slot(result=str)
    def test_connections(self):
        """
        Function tests the settings and connection type set on the UI
        """

        if self.check_online_status():
            # get latest settings
            config.load_settings()

            if os.path.isfile(__config_path__):
                with open(__config_path__) as f:
                    l = pickle.load(f)
                    connections_list = l['connection_types']

            not_working = []

            for con in connections_list:
                con = con.lower()
                lib_path = __plugin_path__+con+'/libs'
                sys.path.append(lib_path)

                plugin_import_cmd = 'import '+con+'_upload_plugin'
                test_upload_cmd = 'if not '+con+'_upload_plugin.'\
    +con.title()+'UploadPlugin().test_upload(): not_working.append(con)'

                try:
                    exec plugin_import_cmd
                    print "Connection test: plugin imported successful"
                except:
                    print "Connection test: plugin import FAILED!"

                # execution string fills not_working list with the not
                # properly working connection's name
                exec test_upload_cmd

            qml_string = ""
            for non in not_working:
                # read plugin name from config file
                with open("/opt/FotoShareN9/plugins/{0}.cfg".format(non)) as cfg:
                    content = cfg.readlines()
                    name = content[0].replace("\n", "")
                    qml_string += "{0}<br>".format(name)

            print qml_string

            # The QML/JS function evaluates and shows the result as dialog
            window.root.show_connection_test_result(qml_string)

        else:
            qml_string = "OFFLINE"
            window.root.show_connection_test_result(qml_string)


    def check_online_status(self):
        mgr = QNetworkConfigurationManager()
        activeConfigs = mgr.allConfigurations(QNetworkConfiguration.Active)
        return mgr.isOnline()


    @QtCore.Slot(str, result=bool)
    def check_connection_active(self, name):
        if os.path.isfile(__config_path__):
            with open(__config_path__) as f:
                l = pickle.load(f)

            connections_list = l['connection_types']

        print name

        if name in connections_list and os.path.isfile('/home/user/.config/FotoShareN9/fotoshare_{0}_plugin.cfg'.format(name.lower())):
            print "Ja"
            return True
        else:
            return False


    @QtCore.Slot(str, result=bool)
    def check_connection_settings(self, name):

        plugins = os.listdir("/home/user/.config/FotoShareN9/")
        name = name.lower()
        name = "fotoshare_"+name+"_plugin.cfg"
        print name

        for i in plugins:
            if i == name:
                return True

        return False


# Starting the app ---------------------------------------------------
if __name__ == '__main__':

    # create folders for saving setting cfg files
    if not os.path.isdir('/home/user/.config/FotoShareN9/'):
        os.makedirs('/home/user/.config/FotoShareN9/')

    # delete resized pics if they become more than 50!
    small_pic_path="/home/user/MyDocs/DCIM/FotoShareN9_small/"

    if os.path.isdir(small_pic_path):
        small_files = os.listdir(small_pic_path)
        if len(small_files) > 50:
            for i in small_files:
                os.remove(small_pic_path+i)
    else:
        os.makedirs(small_pic_path)

    # Start the application.
    app = QtGui.QApplication(sys.argv)

    config = Config()
    main = FotoShareN9()
    plugin = PluginHandler()

    window = QmlWindow()

    sys.exit(app.exec_())
