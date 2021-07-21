import QtQuick 2.15
import QtQuick.Controls 2.15
//import QtQuick.Studio.Effects 1.0
import Qt.labs.qmlmodels 1.0


Item {
    width: 1881
    height: 980

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
            syncView: tableView
            clip: true
            width: contentWidth
            height: tableView.height
            anchors.right: rectangle1.left
            anchors.top: homepage.bottom
            anchors.topMargin: 29
            anchors.rightMargin: 0
        }

        Rectangle {
            id: rectangle1
            x: 77
            y: 70
            height: 217
            color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: homepage.bottom
            anchors.topMargin: 29
            anchors.leftMargin: 73
            anchors.rightMargin: 65

            TableView{
                id: tableHori_header
                x: 0
                y: -1
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
                syncDirection: Qt.Vertical | Qt.Horizontal
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

                //TableViewColumn{}

                ScrollBar.vertical: ScrollBar {
                    id: tableVerticalBar;
                    active: true
                    policy:ScrollBar.AlwaysOn
                }
                /*ScrollBar.horizontal:  ScrollBar {
                    id: tableHorizontal;
                    anchors.top: parent.top
                    wheelEnabled: false
                    spacing: 0
                    anchors.topMargin: 202
                    active: true
                    policy:ScrollBar.AlwaysOn
                }*/

                model: TableModel {
                    TableModelColumn { display: "ip"  }
                    TableModelColumn { display: "mac" }
                    TableModelColumn { display: "id" }
                    TableModelColumn { display: "mes" }
                    TableModelColumn { display: "sdc" }
                    TableModelColumn { display: "ntp" }
                    TableModelColumn { display: "tcp" }
                    TableModelColumn { display: "c_ver" }
                
                /*rows: [
                        {
                            
                        "ip": "125.30.1.1",
                        "mac": "0xD5D5D5D",
                        "id":"0x0009",
                        "mes":"nor",
                        "sdc":"nor",
                        "ntp":"nor",
                        "tcp":"nor",
                        "c_ver":"0x123"
                        },
                        {
                        "ip": "125.30.1.2",
                        "mac": "0xD5D5E5E",
                        "id":"0x0009",
                        "mes":"nor",
                        "sdc":"nor",
                        "ntp":"nor",
                        "tcp":"nor",
                        "c_ver":"0x123"
                    }
                    ]*/
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
    D{i:0;formeditorZoom:0.33}
}
##^##*/
