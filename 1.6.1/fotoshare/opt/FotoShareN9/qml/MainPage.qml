import QtQuick 1.1
import com.nokia.meego 1.0
import com.nokia.extras 1.0

Page {
    id: mainPage
    tools: commonTools
    orientationLock: PageOrientation.LockPortrait

    // Is set to true with MainPages Component.onCompleted signal
    // it prevent the sliders to emit there signal when the page loads.
    property bool page_status: false

    Component.onCompleted: {
        theme.inverted = true
        page_status = true
        console.log("QML: Page (re)loaded, first start function gives the following result:")
        console.log(config.check_not_first_start())
    }

    property string notify: config.check_notification_type_button()
    property int interval_time: config.check_interval_time()

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
        spacing: 90

        Text {
            id: switchText

            anchors.verticalCenter: activateSwitch.verticalCenter
            text: qsTr("Activate FotoShare for N9")
            font.family: "Nokia Pure Text"
            font.pixelSize: 24
            font.bold: true
            color: "lightgrey"
        }

        Switch {
            id: activateSwitch

            enabled: config.check_not_first_start()
            checked: config.check_daemon_running()

            onCheckedChanged: {
                if (page_status === true) {
                    main.start_stop_daemon()
                }
            }
        }
    }

    Row {
        id: onstartupSwitchElement

        anchors.left: parent.left
        anchors.top: activateSwitchElement.bottom
        anchors.leftMargin: 20
        anchors.topMargin: 10
        spacing: 115

        Text {
            id: startupSwitchText

            anchors.verticalCenter: onStartupSwitch.verticalCenter
            text: qsTr("Run daemon on startup")
            font.family: "Nokia Pure Text"
            font.pixelSize: 24
            font.bold: true
            color: "lightgrey"
        }

        Switch {
            id: onStartupSwitch

            checked: config.check_daemon_startup()
            enabled: config.check_not_first_start()

            onCheckedChanged: {
                if (page_status === true) {
                    main.activate_startup_daemon()
                }
            }
        }
    }

    Row {
        id: resizePhotoSwitchElement

        anchors.left: parent.left
        anchors.top: onstartupSwitchElement.bottom
        anchors.leftMargin: 20
        anchors.topMargin: 10
        spacing: 105

        Text {
            id: resizeSwitchText

            anchors.verticalCenter: resizeSwitch.verticalCenter
            text: qsTr("Resize photos on upload")
            font.family: "Nokia Pure Text"
            font.pixelSize: 24
            font.bold: true
            color: "lightgrey"
        }

        Switch {
            id: resizeSwitch

            enabled: config.check_not_first_start()
            checked: config.check_resize_option()

            onCheckedChanged: {
                if (page_status === true) {
                    main.save_resize_option()
                }
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
        stepSize: 10
        value: config.check_resize_percent()
        valueIndicatorVisible: true
        valueIndicatorText: resizeSlider.value+" %"

        enabled: resizeSwitch.checked ? true : false

        //original 'valueChanged' does not work!
        onValueChanged: {
            if (resizeSwitch.enabled && resizeSwitch.checked) {
            main.save_resize_scale(resizeSlider.value)
            console.log("Ich werde verstellt!")
            }
        }
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

        enabled: config.check_not_first_start()

        Button {
            id: notifyOff
            text: "Off"
            onClicked: main.save_notification_type("off")
            checked: notify === "off" ? true : false
        }

        Button {
            id: notifyBanner
            text: "Banner"
            onClicked: main.save_notification_type("banner")
            checked: notify === "banner" ? true : false
        }

        Button {
            id: notifyEvent
            text: "EventFeed"
            onClicked: main.save_notification_type("EventFeed")
            checked: notify === "EventFeed" ? true : false
        }
    }

    ButtonRow {
        id: videoOrNot
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: notificationTypeButton.bottom
        anchors.topMargin: 30

        enabled: config.check_not_first_start()

        Button {
            id: noVideoUploadButton
            text: "No video upload"
            onClicked: main.save_video_upload_option("forbidden")
        }

        Button {
            id: videoUploadButton
            text: "Video upload"
            onClicked: main.save_video_upload_option("allowed")
            checked: config.check_video_upload_button()
        }
    }

    ButtonRow {
        id: wifiOr3G
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: videoOrNot.bottom
        anchors.topMargin: 15

        enabled: config.check_not_first_start()

        Button {
            id: wifiAnd3gButton
            text: "Wifi and 3G"
            onClicked: main.save_wifi3g_option("3G")
        }

        Button {
            id: wifiButton
            text: "Wifi only"
            onClicked: main.save_wifi3g_option("Wlan")
            checked: config.check_connection_type_button()
        }
    }

    ButtonRow {
        id: instantOrInterval
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: wifiOr3G.bottom
        anchors.topMargin: 15

        enabled: config.check_not_first_start()

        Button {
            id: instantButton
            text: "Instant sync"
            onClicked: main.save_upload_type("instant")
        }

        Button {
            id: intervalButton
            text: "Interval sync"
            onClicked: main.save_upload_type("interval")
            checked: config.check_upload_type_button()
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
        opacity: intervalButton.checked ? 1.0 : 0.0

        enabled: config.check_not_first_start()

        Button {
            id: intervalTimeButton5
            text: "5"
            onClicked: main.save_interval_time(intervalTimeButton5.text)
            checked: interval_time === 5 ? true : false
        }

        Button {
            id: intervalTimeButton10
            text: "10"
            onClicked: main.save_interval_time(intervalTimeButton10.text)
            checked: interval_time === 10 ? true : false
        }

        Button {
            id: intervalTimeButton15
            text: "15"
            onClicked: main.save_interval_time(intervalTimeButton15.text)
            checked: interval_time === 15 ? true : false
        }

        Button {
            id: intervalTimeButton30
            text: "30"
            onClicked: main.save_interval_time(intervalTimeButton30.text)
            checked: interval_time === 30 ? true : false
        }

        Button {
            id: intervalTimeButton45
            text: "45"
            onClicked: main.save_interval_time(intervalTimeButton45.text)
            checked: interval_time === 45 ? true : false
        }

        Button {
            id: intervalTimeButton60
            text: "60"
            onClicked: main.save_interval_time(intervalTimeButton60.text)
            checked: interval_time === 60 ? true : false
        }
    }
}
