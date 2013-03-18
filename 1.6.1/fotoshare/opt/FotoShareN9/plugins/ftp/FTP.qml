import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

Page {
    orientationLock: PageOrientation.LockPortrait
    tools: settingsTools

    /*Registering and loading your plugin is mandatory to use your
    functions from <plugin_name>_settings_handler! You can use your 
    functions in the following way:

    <plugin_name>_plugin.<function_name>()

    It's recommended to load directly after reg/load plugin your
    settings on the UI!
    */

    Component.onCompleted: {
        plugin.register_plugin("ftp")
        plugin.load_plugin()

        //JavaScript function implemented in QML
        loadSettings()
    }

    function loadSettings() {
        ftp_plugin.load_settings()

        serverInputField.text = ftp_plugin.server
        portInputField.text = ftp_plugin.port
        pathInputField.text = ftp_plugin.path
        usernameInputField.text = ftp_plugin.username
        passwordInputField.text = ftp_plugin.password
    }

    ToolBarLayout {
        id: settingsTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-back"
            anchors.left: (parent === undefined) ? undefined : parent.left
            onClicked: {
                main.load_services()
                pageStack.pop()
            }
        }
    }

        Text {
        id: title
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 20
        anchors.topMargin: 20

        text: "Settings"
        font.family: "Nokia Pure Text Light"
        font.pixelSize: 40
        color: "#2489e0"
    }

    Text {
        id: subtitle
        anchors.left: parent.left
        anchors.top: title.bottom
        anchors.leftMargin: 20

        color: "lightgrey"
        text: "FTP settings"
        font.pixelSize: 40
        font.family: "Nokia Pure Text Light"
    }

    Column {
        id: fields_server
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 
            serverInputField.activeFocus ||
            portInputField.activeFocus ||
            pathInputField.activeFocus ||
            usernameInputField.activeFocus ||
            passwordInputField.activeFocus ? 20 : 225

        visible: true

        Text {
            id: serverInputTitle
            text: qsTr("Server address:")
            font.pixelSize: 24
            color: "lightgrey"
        }

    Row {
        id: serverInputRow
        spacing: 10

        TextField {
            id: serverInputField
            width: 350
            placeholderText: qsTr("type in your server adress")
        }

        TextField {
            id: portInputField
            width: 80
            placeholderText: qsTr("port")
            inputMethodHints: Qt.ImhDigitsOnly
        }
    }

        Text {
            id: pathInputTitle

            text: qsTr("Folder on server for saving:")
            font.pixelSize: 24
            color: "lightgrey"
        }

        TextField {
            id: pathInputField

            width: 440
            placeholderText: qsTr("specify a path to a folder")
        }

        Text {
            id: usernameInputTitle

            text: qsTr("Username:")
            font.pixelSize: 24
            color: "lightgrey"
        }

        TextField {
            id: usernameInputField

            width: 440
            placeholderText: qsTr("type in your username")
        }

        Text {
            id: passwordInputTitle

            text: qsTr("Password:")
            font.pixelSize: 24
            color: "lightgrey"
        }

        TextField {
            id: passwordInputField

            width: 440
            echoMode: TextInput.Password
            placeholderText: qsTr("type in your password")
        }
    }

    Button {
        id: saveSettingsButton
        objectName: "saveSettingsButton"

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 600
        text: qsTr("Save settings")

        onClicked: {
                var serverdata = serverInputField.text
                var portdata = portInputField.text
                var pathdata = pathInputField.text
                var userdata = usernameInputField.text
                var passdata = passwordInputField.text

                ftp_plugin.save_settings(serverdata, portdata, pathdata, userdata, passdata)

                if (serverdata === ""){
                    noServerWarningDialog.open();
                    ftp_plugin.delete_settings()
            }
        }
    }

    QueryDialog {
        id: noServerWarningDialog
        titleText: "Information"
        message: "You've not specified a server. If you don't want, that FotoShareN9 uploads to your server anymore: everything is fine. Otherwise you should check your settings! ;)"
        acceptButtonText: "Ok"
    }
}

