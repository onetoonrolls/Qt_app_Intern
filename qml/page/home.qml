import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import Qt.labs.qmlmodels 1.0


Item {
    width: Screen.desktopAvailableWidth -69
    height: Screen.desktopAvailableHeight -108
    //width: 1821
    //height: 1000

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

            TableView{
                id: tableHori_header
                x: 0
                y: -1
                syncView: tableView
                width: tableView.width
                height: 30
                anchors.bottom: tableView.top
                anchors.bottomMargin: 0
                synchronousDrag: false
                pixelAligned: false
                boundsBehavior: Flickable.StopAtBounds
                columnSpacing: 1
                rowSpacing: 1
                clip: true
                syncDirection: Qt.Horizontal
                model: TableModel {
                    TableModelColumn { display: "keyvalue1" }
                    TableModelColumn { display: "keyvalue2" }
                    TableModelColumn { display: "keyvalue3" }
                    TableModelColumn { display: "keyvalue4" }
                    TableModelColumn { display: "keyvalue5" }
                    TableModelColumn { display: "keyvalue6" }
                    TableModelColumn { display: "keyvalue7" }
                    TableModelColumn { display: "keyvalue8" }
                rows: [{
                        "keyvalue1" : "Ip address",
                        "keyvalue2" : "Mac address",
                        "keyvalue3" : "Device ID",
                        "keyvalue4" : "MES status",
                        "keyvalue5" : "SDC status",
                        "keyvalue6" : "NTP updata",
                        "keyvalue7" : "TCP updata",
                        "keyvalue8" : "Firmware version",
                  }]
                }
                delegate:  DelegateChooser{
                    DelegateChoice{
                        row: 0
                        delegate: Rectangle{
                            implicitWidth: 215
                            implicitHeight: 30
                            border.width: 1
                            color: "#ff1e1e"
                            Text{
                                text: model.display == null? "":model.display
                                color: "#000000"
                                font.pixelSize : 20
                                anchors.centerIn: parent
                            }
                        }
                    }
                }
            }

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

                model: TableModel {
                    TableModelColumn { display: "ip"  }
                    TableModelColumn { display: "mac" }
                    TableModelColumn { display: "id" }
                    TableModelColumn { display: "mes" }
                    TableModelColumn { display: "sdc" }
                    TableModelColumn { display: "ntp" }
                    TableModelColumn { display: "tcp" }
                    TableModelColumn { display: "c_ver" }
                
                }

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
                Component.onCompleted: console.log("device table home created ")
            }
        }
    }

    Connections{
        target: homeBackend

        function onSetContextTable(ip,mac,id,mes,sdc,ntp,tcp,c_ver){
            //print("data revive in home : ",ip,mac,id,mes,sdc,ntp,tcp,c_ver)
            //tableView.model.clear()
            tableView.model.appendRow({
                "ip":ip,
                "mac":mac,
                "id":id,
                "mes":mes,
                "sdc":sdc,
                "ntp":ntp,
                "tcp":tcp,
                "c_ver":c_ver,
            }) 
            
        }
        
        function onSetBoolDeviceClear(state_btn){
                print("clear device done")
                tableView.model.clear()
            }
     }
 }








/*##^##
Designer {
    D{i:0;formeditorZoom:0.33}D{i:4}
}
##^##*/
