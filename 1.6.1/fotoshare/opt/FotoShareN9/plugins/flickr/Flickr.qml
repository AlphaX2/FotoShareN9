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
    */

    Component.onCompleted: {
        plugin.register_plugin("flickr")
        plugin.load_plugin()

        // JavaScript function to set the authentification buttons
        // text related to actual state (linked / not linked). Gets
        // data from Qt Property via Python
        set_auth_button_text()
    }

    function set_auth_button_text() {
            var button_text = flickr_plugin.get_button_text()
            flickrAuthButton.text = button_text
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
        text: "Flickr settings"
        font.pixelSize: 40
        font.family: "Nokia Pure Text Light"
    }

        Image {
        id: flickrLogo

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 350
        source: "img/flickr-icon.png"
        width: 256
        height: 256
    }

    Button {
        id: flickrAuthButton

        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottomMargin: 280
        text: "Link Flickr"

        onClicked: {
            var status = flickrAuthButton.text

            // part 1 opens auth web page
            if (status === "Link Flickr") {
                flickr_plugin.auth_flickr_part1()
                flickrAuthButton.text = "Ok"
                }
            // part 2 saves the returned token
            if (status === "Ok") {
                flickr_plugin.auth_flickr_part2()
                flickrAuthButton.text = "Unlink Flickr"
                }
            // unlink will delete token file
            if (status === "Unlink Flickr") {
                flickr_plugin.unlink_flickr()
                flickrAuthButton.text = "Link Flickr"
                }
        }
    }

    Text {
        id: flickrTermsOfServiceLink

        anchors.top: flickrAuthButton.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 100
        text: "Flickr Terms of Service"
        color: openTermsLink.pressed ? "darkgrey" : "white"
        font.pixelSize: 24
        font.bold: true
        visible: true

        MouseArea {
            id: openTermsLink
            anchors.fill: parent
            onClicked: {Qt.openUrlExternally("http://www.flickr.com/help/terms/")}
        }
    }

    Text {
        id: flickrPrivacyPolicy

        anchors.top: flickrAuthButton.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: 150
        text: "Flickr privacy policy"
        color: openPrivacyLink.pressed ? "darkgrey" : "white"
        font.pixelSize: 24
        font.bold: true
        visible: true

        MouseArea {
            id: openPrivacyLink
            anchors.fill: parent
            onClicked: {Qt.openUrlExternally("http://www.flickr.com/help/privacy-policy/")}
        }
    }
}
