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
        
        function delay(delayTime) {
        
            timer.interval = delayTime
            timer.start()
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
    }

    Timer{
         id: timer
         running: true
         repeat: false
         //onTriggered: console.log("timer running")

    }

    Connections{
        target: homeBackend
        
     }
 }








/*##^##
Designer {
    D{i:0;formeditorZoom:0.33}D{i:4}
}
##^##*/
