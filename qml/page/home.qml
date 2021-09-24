import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import Qt.labs.qmlmodels 1.0
import QtQml 2.15

Item {
    width: Screen.desktopAvailableWidth -69
    height: Screen.desktopAvailableHeight -108
    //width: 1821
    //height: 1000
    QtObject{
        id:internal
        property bool notiset: false
        function delay(delayTime) {

            timer.interval = delayTime
            timer.start()
        }

        function getFirstIndex(model) {
            if(internal.notiset | model.count>1){
                //console.log("toggole 1")
                var contex = model.get(1).data
                model.remove(1)
                internal.notiset = false
            }
            else{
                //console.log("toggle 0")
                var contex = model.get(0).data
            }
            return contex
        }

    }
    Rectangle {
        id: rectangle
        width: 1880
        color: "#202020"
        border.color: "#00000000"
        anchors.fill: parent

        Label {
            id: homepage
            width: 378
            height: 46
            color: "#ffffff"
            text: qsTr("Home page")
            anchors.left: parent.left
            anchors.top: parent.top
            horizontalAlignment: Text.AlignHCenter
            anchors.leftMargin: 0
            anchors.topMargin: 0
            font.pointSize: 20
        }
        
        VerticalHeaderView {
            id: verticalHeader
            width: 30
            syncView: tableView
            clip: true
            height: tableView.height
            anchors.right: tableDevice.left
            anchors.top: homepage.bottom
            anchors.topMargin: 29
            anchors.rightMargin: 0
        }

        HorizontalHeaderView {
            id: horiHeader
            x: tableDevice.x
            width: tableView.width
            syncView: tableView
            clip: true
            height: 30
            anchors.bottom: tableDevice.top
            anchors.bottomMargin: 0
        }

        Rectangle {
            id: tableDevice
            x: 77
            y: 70
            height: 217
            color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: homepage.bottom
            anchors.rightMargin: 65
            anchors.topMargin: 29
            anchors.leftMargin: 73

            TableView {
                id: tableView
                x: 0
                y: 29
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.rightMargin: 0
                synchronousDrag: false
                pixelAligned: false
                boundsBehavior: Flickable.StopAtBounds
                anchors.bottomMargin: 0
                anchors.leftMargin: 0
                anchors.topMargin: 0
                columnSpacing: 1
                rowSpacing: 1
                clip: true
                syncDirection: Qt.Vertical | Qt.Horizontal

                ScrollBar.vertical: ScrollBar {
                    id: tableVerticalBar;
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    active: true
                    //policy:ScrollBar.AlwaysOnS
                    clip: true
                }

                model: DeviceModel

                delegate:  DelegateChooser{
                    DelegateChoice{
                        //row: 0
                        delegate: Rectangle{
                            implicitWidth: 215
                            implicitHeight: 50
                            border.width: 1
                            color: "#FFFFFF"
                            Text{
                                text: model.display == null? "":model.display
                                minimumPixelSize: 20
                                color: "#000000"
                                font.pixelSize : 20
                                anchors.centerIn: parent
                            }
                        }
                    }
                }
                //Component.onCompleted: console.log("device table home created ")
            }
        }
        VerticalHeaderView {
            id: verticalHeaderLog
            y: tableLog.y
            width: 30
            syncView: logFTP
            clip: true
            height: tableLog.height
            anchors.right: tableLog.left
            anchors.rightMargin: 0
        }

        HorizontalHeaderView {
            id: horiHeaderLog
            x: tableLog.x
            width: tableLog.width
            syncView: logFTP
            clip: true
            height: 30
            anchors.bottom: tableLog.top
            anchors.bottomMargin: 0
        }
        Rectangle {
            id: nitoUpStatus
            x: tableDevice.x
            width: 500
            height: 40
            color: "#555555"
            border.color: "#00000000"
            anchors.top: tableDevice.bottom
            anchors.topMargin: 16

            Label{
                y: 0
                width: 341
                height: 46
                color: "#ffffff"
                text: "Notification Update"
                anchors.left: parent.left
                anchors.leftMargin: 20
                font.pointSize: 20
            }
        }

        Rectangle {
            id: nitoUpStatuscontext
            y: nitoUpStatus.y
            height: 40
            color: "#7d7d7d"
            border.color: "#00000000"
            anchors.left: nitoUpStatus.right
            anchors.right: parent.right
            anchors.rightMargin: 65
            anchors.leftMargin: 0


            Label{
                id: contextNoti
                x: 0
                y: 0
                width: nitoUpStatuscontext.width
                height: nitoUpStatuscontext.height
                color: "#ffffff"
                font.pointSize: 20
            }
        }
        Rectangle{
            id: tableLog
            x: tableDevice.x
            height: 460
            color: "#00000000"
            border.color: "#00000000"
            width: rectangle.width/2
            anchors.top: nitoUpStatus.bottom
            anchors.topMargin: 40
            TableView{
                id: logFTP
                anchors.fill: parent
                synchronousDrag: false
                pixelAligned: false
                boundsBehavior: Flickable.StopAtBounds
                columnSpacing: 1
                rowSpacing: 1
                clip: true
                syncDirection: Qt.Vertical | Qt.Horizontal

                ScrollBar.vertical: ScrollBar {
                    id: logVerticalBar
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    active: true
                    //policy:ScrollBar.AlwaysOnS
                    clip: true
                }

                model: LogFTPModel

                delegate:  DelegateChooser{
                    DelegateChoice{
                        //row: 0
                        delegate: Rectangle{
                            implicitWidth: 215
                            implicitHeight: 50
                            border.width: 1
                            color: "#FFFFFF"
                            Text{
                                text: model.display == null? "":model.display
                                minimumPixelSize: 20
                                color: "#000000"
                                font.pixelSize : 20
                                anchors.centerIn: parent
                            }
                        }
                    }
                }
            }
        }

        Rectangle {
            id: regist
            y: tableLog.y
            height: 450
            color: "#515151"
            anchors.left: tableLog.right
            anchors.right: parent.right
            anchors.top: nitoUpStatuscontext.bottom
            anchors.leftMargin: 88
            anchors.rightMargin: 65
            anchors.topMargin: 40

            Rectangle {
                id: rectangle1
                height: 48
                color: "#353535"
                radius: 32.5
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: deviceHead.bottom
                anchors.leftMargin: 56
                anchors.rightMargin: 38
                anchors.topMargin: 8

                TextInput {
                    id: textDN
                    x: 20
                    y: 181
                    width: 500
                    height: 35
                    color: "#ffffff"
                    text: qsTr("insert Device name")
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 25
                }
            }

            Rectangle {
                id: rectangle3
                height: 48
                color: "#353535"
                radius: 0
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                anchors.topMargin: 0
            }

            Rectangle {
                id: rectangle2
                height: 48
                color: "#353535"
                radius: 32.5
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: ipHead.bottom
                anchors.leftMargin: 56
                anchors.rightMargin: 38
                anchors.topMargin: 8

                TextInput {
                    id: textIP
                    x: 20
                    y: 7
                    width: 500
                    height: 35
                    color: "#ffffff"
                    text: qsTr("insert IP Address")
                    anchors.verticalCenter: parent.verticalCenter
                    font.pixelSize: 25
                }
            }

            Label {
                id: registHead
                x: 2
                width: 367
                height: 46
                color: "#ffffff"
                text: "Add devices section"
                anchors.left: cir.right
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.leftMargin: 5
                font.pointSize: 20


            }

            Label {
                id: ipHead
                x: 2
                width: 181
                height: 46
                color: "#ffffff"
                text: "IP Address"
                anchors.left: parent.left
                anchors.top: registHead.bottom
                anchors.topMargin: 10
                anchors.leftMargin: 34
                font.pointSize: 20
            }

            Label {
                id: deviceHead
                x: 2
                width: 181
                height: 46
                color: "#ffffff"
                text: "Device name"
                anchors.left: parent.left
                anchors.top: ipHead.bottom
                anchors.topMargin: 61
                anchors.leftMargin: 34
                font.pointSize: 20
            }

            Row {
                id: row
                x: 328
                width: 322
                height: 60
                anchors.right: parent.right
                anchors.top: deviceHead.bottom
                anchors.topMargin: 115
                anchors.rightMargin: 50
                spacing: 15

                Button {
                    id: regist_con
                    width: 150
                    height: 50
                    text: qsTr("confirm")
                    font.pointSize: 15
                    checked: false
                    onClicked:{
                        if(textIP.text =="" | textDN.text == ""){
                            contextNotitext.append({"data": "input box is null"})
                            internal.notiset = true
                            //contextNoti.text = "input box is null"
                        }
                        else{
                            homeBackend.registDevice(textIP.text,textDN.text)
                        }
                            
                    }
                }

                Button {
                    id: regist_cancle
                    width: 150
                    height: 50
                    text: qsTr("cancle")
                    font.pointSize: 15
                    checked: false
                    onClicked:{
                        textIP.text = ""
                        textDN.text = ""
                    }
                }
            }

            Rectangle {
                id: cir
                width: 30
                height: 30
                color: "#fe3434"
                radius: 18.5
                border.color: "#00000000"
                border.width: 2
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.leftMargin: 5
                anchors.topMargin: 8
            }
        }
    }
    
    Timer{
        id: timer
        running: true
        repeat: false
        //onTriggered: console.log("timer running")

    }

    ListModel {
        id: contextNotitext
        ListElement {
            data: ""
        }       
    }

    Timer{
        id: timerNoti
        running: true
        repeat: true
        interval : 8000
        onTriggered:{
            contextNoti.text = internal.getFirstIndex(contextNotitext)
        }
    }

    Connections{
        target: homeBackend

        function onSetContexNoti(context){
            contextNotitext.append({"data": context})
            internal.notiset = true
            //contextNoti.text = context
        }
        
    }
}








/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}D{i:27}D{i:30}D{i:26}
}
##^##*/
