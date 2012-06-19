import QtQuick 1.1
import com.nokia.meego 1.0
import Qt 4.7

Page {
    id: settingsWindow
    tools: settingsTools
    orientationLock: PageOrientation.LockPortrait

    property alias ftpChecked: ftpConButton.checked
    property alias sftpChecked: sftpConButton.checked
    property alias scpChecked: scpConButton.checked
    property alias dropboxChecked: dropboxConButton.checked

    property alias serverField: serverInputField.text
    property alias pathField: pathInputField.text
    property alias userField: usernameInputField.text
    property alias passField: passwordInputField.text
    property alias portField: portInputField.text
    property alias conButton: testConnectionButton.opacity
    property alias authButton: dropboxAuthButton.text

    property string dropboxURL: ""
    property string selectedConnectionType : "ftp"

    ToolBarLayout {
        id: settingsTools
        visible: true
        ToolIcon {
            platformIconId: "toolbar-back"
            anchors.left: (parent === undefined) ? undefined : parent.left
            onClicked: {
                //If daemon running, it will be stopped, due to server changes!
                mainPage.switcherCHECK = false
                pageStack.pop()
            }
        }
    }

    Text {
        id: title
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        anchors.leftMargin: 20
        anchors.bottomMargin:
            serverInputField.activeFocus ||
            portInputField.activeFocus ||
            pathInputField.activeFocus ||
            usernameInputField.activeFocus ||
            passwordInputField.activeFocus ? 465 : 670

        text: "Settings"
        font.family: "Nokia Pure Text Light"
        font.pixelSize: 48
        color: "#2489e0"
    }

    ButtonRow {
        id: connectionTypeButton
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin:
            serverInputField.activeFocus ||
            portInputField.activeFocus ||
            pathInputField.activeFocus ||
            usernameInputField.activeFocus ||
            passwordInputField.activeFocus ? 395 : 600

        Button {
            id: dropboxConButton
            text: "Dropbox"
            font.pixelSize: 23
        }

        Button {
            id: ftpConButton
            text: "FTP"
            font.pixelSize: 23
            onClicked: selectedConnectionType = "ftp"
        }

        Button {
            id: sftpConButton
            text: "sFTP"
            font.pixelSize: 23
            onClicked: selectedConnectionType = "sftp"
        }

        Button {
            id: scpConButton
            text: "Scp"
            font.pixelSize: 23
            onClicked: selectedConnectionType = "scp"
        }
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
        visible: dropboxConButton.checked ? false : true

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

    Image {
        id: dropboxLogo

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 350
        source: "Dropbox-Logo.png"
        visible: dropboxConButton.checked ? true: false
        width: 400
        height: 150
    }

    Button {
        id: dropboxAuthButton

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 300
        text: "Link Dropbox"
        visible: dropboxConButton.checked ? true: false
        onClicked: {
            var state = dropboxAuthButton.text

            if (state === "Link Dropbox"){controller.auth_dropbox_signal("web")}
            if (state === "Ok"){
                    controller.auth_dropbox_signal("save")

                    //enable all buttons on UI
                    mainPage.switcherENABLE = true
                    mainPage.switcherStartupENABLE = true
                    mainPage.switcherResizeENABLE = true
                    mainPage.notifyButtonENABLE = true
                    mainPage.videoUploadENABLE = true
                    mainPage.uploadTypeButtonENABLE = true
                    mainPage.wifi3GENABLE = true

                    testConnectionButton.opacity = 1.0
                }

            if (state === "Unlink Dropbox"){controller.auth_dropbox_signal("unlink")}
        }
    }

    Text {
        id: dropboxAuthURL

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 200
        text: dropboxAuthButton.text === "Ok" ? "Click here to connect Dropbox<br>then came back and press 'Ok'." : ""
        color: openLink.pressed ? "darkgrey" : "white"
        font.pixelSize: 24
        visible: dropboxConButton.checked ? true: false

        MouseArea {
            id: openLink
            anchors.fill: parent
            onClicked: {Qt.openUrlExternally(dropboxURL)
            }
        }
    }

    Button {
        id: saveSettingsButton
        objectName: "saveSettingsButton"

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 600
        text: qsTr("Save settings")
        visible: dropboxConButton.checked ? false: true

        onClicked: {
                var serverdata = serverInputField.text
                var pathdata = pathInputField.text
                var userdata = usernameInputField.text
                var passdata = passwordInputField.text
                var portdata = portInputField.text
                var connect = selectedConnectionType

                controller.save_settings_signal(serverdata, pathdata, userdata, passdata, connect, portdata)

                //enable all buttons on UI

                // Main activation switcher
                mainPage.switcherENABLE = true
                mainPage.switcherStartupENABLE = true
                mainPage.switcherResizeENABLE = true
                mainPage.notifyButtonENABLE = true
                mainPage.videoUploadENABLE = true
                mainPage.uploadTypeButtonENABLE = true
                mainPage.wifi3GENABLE = true

                testConnectionButton.opacity = 1.0

                if (serverdata === ""){noServerWarningDialog.open()}
                else {startDaemonAgainDialog.open()}
        }
    }

    Button {
        id: testConnectionButton

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: saveSettingsButton.bottom
        anchors.topMargin: 10
        text: qsTr("Test connection")

        onClicked: {
            if (dropboxConButton.checked) {controller.test_connection_signal("Dropbox")}
            else {controller.test_connection_signal(String(selectedConnectionType))}
        }
    }

    QueryDialog {
        id: startDaemonAgainDialog
        titleText: "Information"
        message: "You have to activate FotoShareN9 again, because you've changed your server settings. So go back to the main page and switch the slider or FotoShare is not running anymore!"
        acceptButtonText: "Ok"
    }

    QueryDialog {
        id: noServerWarningDialog
        titleText: "Information"
        message: "You've not specified a server. If you don't want, that FotoShareN9 uploads to your server anymore: everything is fine. Otherwise you should check your settings! ;)"
        acceptButtonText: "Ok"
    }
}

