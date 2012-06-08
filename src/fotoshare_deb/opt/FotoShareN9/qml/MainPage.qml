import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

Page {
    tools: commonTools
    orientationLock: PageOrientation.LockPortrait
    Component.onCompleted: {theme.inverted = true}

    property alias switcherENABLE: activateSwitch.enabled
    property alias switcherCHECK: activateSwitch.checked

    //will be enabled if FotoShare is activated (above Switcher)
    property alias switcherStartupENABLE: onStartupSwitch.enabled
    property alias switcherStartupCHECK: onStartupSwitch.checked

    property alias switcherResizeENABLE: resizeSwitch.enabled
    property alias switcherResizeCHECK: resizeSwitch.checked
    property alias resizeSliderValue: resizeSlider.value

    //Button Rows with more options

    property alias notifyButtonENABLE: notificationTypeButton.enabled
    property alias notifyButtonOffCHECK: notifyOff.checked
    property alias notifyButtonBannerCHECK: notifyBanner.checked
    property alias notifyButtonEventCHECK: notifyEvent.checked

    property alias videoUploadENABLE: videoOrNot.enabled
    property alias videoUploadCHECK: videoUploadButton.checked

    property alias wifi3GENABLE: wifiOr3G.enabled
    property alias wifiCHECK: wifiButton.checked

    property alias uploadTypeButtonENABLE: instantOrInterval.enabled
    property alias intervalButtonCHECK: intervalButton.checked

    property alias interval5: intervalTimeButton5.checked
    property alias interval10: intervalTimeButton10.checked
    property alias interval15: intervalTimeButton15.checked
    property alias interval30: intervalTimeButton30.checked
    property alias interval45: intervalTimeButton45.checked
    property alias interval60: intervalTimeButton60.checked

    Text {
        id: appTitle

        anchors.top: parent.top
        anchors.left: parent.left
        anchors.topMargin: 10
        anchors.leftMargin: 20
        text: "FotoShareN9"
        font.family: "Nokia Pure Text Light"
        font.pixelSize: 48
        color: "#2489e0"
    }

    Row {
        id: activateSwitchElement

        anchors.left: parent.left
        anchors.top: appTitle.bottom
        anchors.leftMargin: 20
        anchors.topMargin: 10
        spacing: 20

        Text {
            id: switchText

            verticalAlignment: Text.AlignVCenter
            text: qsTr("Activate FotoShare for N9")
            font.family: "Nokia Pure Text Light"
            font.pixelSize: 32
            color: "lightgrey"
        }

        Switch {
            id: activateSwitch
            objectName: "switchToogle"

            enabled: false
            onCheckedChanged: {
                controller.start_daemon_signal()
            }
        }
    }

    Row {
        id: onstartupSwitchElement

        anchors.left: parent.left
        anchors.top: activateSwitchElement.bottom
        anchors.leftMargin: 20
        anchors.topMargin: 10
        spacing: 45

        Text {
            id: startupSwitchText

            verticalAlignment: Text.AlignVCenter
            text: qsTr("Run daemon on startup")
            font.family: "Nokia Pure Text Light"
            font.pixelSize: 32
            color: "lightgrey"
        }

        Switch {
            id: onStartupSwitch
            objectName: "switchToogle"

            enabled: false
            onCheckedChanged: {
                controller.activate_startup_daemon_signal()
            }
        }
    }

    Row {
        id: resizePhotoSwitchElement

        anchors.left: parent.left
        anchors.top: onstartupSwitchElement.bottom
        anchors.leftMargin: 20
        anchors.topMargin: 10
        spacing: 35

        Text {
            id: resizeSwitchText

            verticalAlignment: Text.AlignVCenter
            text: qsTr("Resize photos on upload")
            font.family: "Nokia Pure Text Light"
            font.pixelSize: 32
            color: "lightgrey"
        }

        Switch {
            id: resizeSwitch
            objectName: "switchToogle"

            enabled: false
            onCheckedChanged: {
                if (resizeSwitch.checked) {controller.resize_photos_signal(50)}
                else {controller.resize_photos_signal(0)}
            }
        }
    }

    Slider {
        id: resizeSlider
        anchors.top: resizePhotoSwitchElement.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.topMargin: resizeSwitch.checked ? 0 : -60

        visible: resizeSwitch.checked ? true : false
        maximumValue: 90
        minimumValue: 10
        value: 50
        stepSize: 10
        valueIndicatorVisible: true
        valueIndicatorText: resizeSlider.value+" %"

        //original 'valueChanged' does not work!
        onValueChanged: controller.resize_photos_signal(resizeSlider.value)
    }

    Rectangle {
        id: spacer1
        anchors.top: resizeSlider.bottom
        anchors.topMargin: 10
        width: parent.width
        height: 2
        color: "darkgrey"
    }

    Text {
        id: notificationTypeText
        anchors.left: parent.left
        anchors.top: spacer1.bottom
        anchors.leftMargin: 20
        anchors.topMargin: 5

        text: "Notification type:"
        color: "white"
        font.pixelSize: 24
        font.family: "Nokia Pure Text Light"
    }

    ButtonRow {
        id: notificationTypeButton
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: notificationTypeText.bottom
        anchors.topMargin: 10
        enabled: false

        Button {
            id: notifyOff
            text: "Off"
            onClicked: controller.notification_select_signal("off")
        }

        Button {
            id: notifyBanner
            text: "Banner"
            onClicked: controller.notification_select_signal("banner")
        }

        Button {
            id: notifyEvent
            text: "EventFeed"
            onClicked: controller.notification_select_signal("EventFeed")
        }
    }

    ButtonRow {
        id: videoOrNot
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: notificationTypeButton.bottom
        anchors.topMargin: 30
        enabled: false

        Button {
            id: noVideoUploadButton
            text: "No video upload"
            onClicked: controller.video_select_signal("forbidden")
        }

        Button {
            id: videoUploadButton
            text: "Video upload"
            onClicked: controller.video_select_signal("allowed")
        }
    }

    ButtonRow {
        id: wifiOr3G
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: videoOrNot.bottom
        anchors.topMargin: 15
        enabled: false

        Button {
            id: wifiAnd3gButton
            text: "Wifi and 3G"
            onClicked: controller.wifi3g_select_signal("3G")
        }

        Button {
            id: wifiButton
            text: "Wifi only"
            onClicked: controller.wifi3g_select_signal("Wlan")
        }
    }

    ButtonRow {
        id: instantOrInterval
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: wifiOr3G.bottom
        anchors.topMargin: 15
        enabled: false

        Button {
            id: instantButton
            text: "Instant sync"
            onClicked: controller.upload_type_select_signal("instant")
        }

        Button {
            id: intervalButton
            text: "Interval sync"
            onClicked: controller.upload_type_select_signal("interval")
        }
    }

    Text {
        id: intervalSelectionTitle
        anchors.left: parent.left
        anchors.top: instantOrInterval.bottom
        anchors.leftMargin: 20
        anchors.topMargin: 10

        font.pixelSize: 24
        font.family: "Nokia Pure Text Light"
        text: "Interval in minutes:"
        color: "white"
        opacity: intervalSelection.opacity
    }

    ButtonRow {
        id: intervalSelection
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: intervalSelectionTitle.bottom
        anchors.topMargin: 10
        opacity: intervalButton.checked ? 1 : 0

        Button {
            id: intervalTimeButton5
            text: "5"
            onClicked: controller.save_interval_time_signal(intervalTimeButton5.text)
        }

        Button {
            id: intervalTimeButton10
            text: "10"
            onClicked: controller.save_interval_time_signal(intervalTimeButton10.text)
        }

        Button {
            id: intervalTimeButton15
            text: "15"
            onClicked: controller.save_interval_time_signal(intervalTimeButton15.text)
        }

        Button {
            id: intervalTimeButton30
            text: "30"
            onClicked: controller.save_interval_time_signal(intervalTimeButton30.text)
        }

        Button {
            id: intervalTimeButton45
            text: "45"
            onClicked: controller.save_interval_time_signal(intervalTimeButton45.text)
        }

        Button {
            id: intervalTimeButton60
            text: "60"
            onClicked: controller.save_interval_time_signal(intervalTimeButton60.text)
        }
    }

    //ALTERNATIVE TO TOOLBUTTON!
/*    Button {
        id: settingsButton
        objectName: "settingsButton"

        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20
        text: qsTr("Server settings")

        onClicked: {
            controller.load_settings_signal()
            pageStack.push(settingsPage)
        }
    }*/
}
