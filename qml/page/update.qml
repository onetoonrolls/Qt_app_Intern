import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.qmlmodels 1.0

Item {
    width: 1881
    height: 980

    QtObject{
        id: internal
        property string typeConnect: ""
        function findIndex(myModel,searchedId){
            for(var i = 0; i < myModel.count; i++) {
                //print("count ",i)
                var elemCur = myModel.get(i).name;
                print(elemCur)
                if(searchedId == elemCur) {
                    print("Found it at index : ", i)
                    return i
                }
                else{
                    print("not found name")
                }
            }
        }
        function findMac(myModel,searchedIP){
            var index =0
            for(var i =0; i < myModel.model.rowCount ; i++){
                if(myModel.model.rows[i].ip == searchedIP)
                    index = i
                else{
                    print("ip not match")
                }
            }
            print("mac in table : ",myModel.model.rows[index].mac)
            return myModel.model.rows[index].mac
        }
        function getAllitemlist(myModel){
            for(var i = 0; i < myModel.count; i++){
                print("Item list : ",myModel.get(i).name)
                UpdatbackEnd.getUpdateIP(myModel.get(i).name)
            }
        }
        function unCheckBox(myModel){
            for(var i=0; i< myModel.count;i++){
                myModel.setProperty(i, "ischecked", false)
            }
        }
    }

    Rectangle {
        id: rectangle
        color: "#202020"
        border.color: "#00000000"
        anchors.fill: parent
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0

        Label {
            id: updatepage
            x: 0
            y: 0
            width: 263
            height: 46
            color: "#ffffff"
            text: qsTr("Update page")
            anchors.verticalCenter: parent.verticalCenter
            horizontalAlignment: Text.AlignHCenter
            anchors.verticalCenterOffset: -467
            anchors.horizontalCenterOffset: -809
            font.pointSize: 20
            anchors.horizontalCenter: parent.horizontalCenter
        }

        Row {
            id: confirmBtn
            x: 1200
            width: 681
            height: 82
            anchors.right: parent.right
            anchors.top: updateOption.bottom
            anchors.topMargin: 20
            spacing: 18
            anchors.rightMargin: 0

            Button {
                id: updateNow
                width: 150
                height: 65
                text: "update Now"
                onClicked: {
                    internal.getAllitemlist(listmodelId)
                    print("send IP to python")
                    contextNoti.text = "Processing to python backend"
                    UpdatbackEnd.updateFirmware(internal.typeConnect)
                }
            }

            Button {
                id: setTime
                width: 150
                height: 65
                text: "set time"
            }

            Button {
                width: 150
                height: 65
                id: cancle
                text: "cancle"
                onClicked: {
                    internal.unCheckBox(comboList)
                }
            }
        }

        Rectangle {
            id: nitoUpStatus
            width: 500
            height: 40
            color: "#555555"
            border.color: "#00000000"
            anchors.left: parent.left
            anchors.top: deviceTable.bottom
            anchors.topMargin: 10
            anchors.leftMargin: 73
            Label{
                width: 263
                height: 46
                color: "#ffffff"
                text: "Notification Update"
                anchors.left: parent.left
                anchors.leftMargin: 20
                font.pointSize: 20
            }
        }

        VerticalHeaderView {
            id: verticalHeader
            syncView: tableView
            clip: true
            width: contentWidth
            height: tableView.height
            anchors.right: deviceTable.left
            anchors.top: updatepage.bottom
            anchors.topMargin: 29
            anchors.rightMargin: 0
        }
        Rectangle {
            id: deviceTable
            height: 217
            color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: updatepage.bottom
            anchors.topMargin: 29
            anchors.rightMargin: 65
            anchors.leftMargin: 73

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
            }

        }

        Rectangle {
            id: nitoUpStatuscontext
            height: 40
            color: "#7d7d7d"
            border.color: "#00000000"
            anchors.left: nitoUpStatus.right
            anchors.right: parent.right
            anchors.top: deviceTable.bottom
            anchors.topMargin: 10
            anchors.rightMargin: 65
            anchors.leftMargin: 1

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

        VerticalHeaderView {
            id: statusVerticalHeader
            x: 198
            y: 379
            syncView: tableStatus
            clip: true
            width: contentWidth
            height: tableStatus.height
            anchors.right: notiTable.left
            anchors.top: nitoUpStatuscontext.bottom
            anchors.topMargin: 48
            anchors.rightMargin: 0
        }
        Rectangle {
            id: notiTable
            y: 368
            height: 200
            color: "#00000000"
            border.color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: nitoUpStatus.bottom
            anchors.rightMargin: 65
            anchors.leftMargin: 73
            anchors.topMargin: 40

            TableView{
                id: tablestatusHori_header
                x: 0
                y: -22
                width: tableStatus.width
                height: 30
                anchors.bottom: tableStatus.top
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
                    rows: [{
                            "keyvalue1" : "IP address",
                            "keyvalue2" : "MAC address",
                            "keyvalue3" : "Date",
                            "keyvalue4" : "Error code"
                        }]

                }

                delegate:  DelegateChooser{
                    DelegateChoice{
                        row: 0
                        delegate: Rectangle{
                            implicitWidth: 300
                            implicitHeight: 30
                            border.width: 1
                            color: "#8cff8e"
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
                id: tableStatus
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.rightMargin: 99
                anchors.leftMargin: 0
                anchors.bottomMargin: 0
                anchors.topMargin: 8
                contentWidth: 900
                synchronousDrag: false
                pixelAligned: false
                boundsBehavior: Flickable.StopAtBounds
                columnSpacing: 1
                rowSpacing: 1
                clip: true
                syncDirection: Qt.Vertical | Qt.Horizontal

                ScrollBar.vertical: ScrollBar {
                    id: tablestatusVerticalBar;
                    x: 1200
                    height: tableStatus.height
                    active: true
                    policy:ScrollBar.AlwaysOn
                }

                model: TableModel {
                    TableModelColumn { display: "ip"  }
                    TableModelColumn { display: "mac" }
                    TableModelColumn { display: "date"}
                    TableModelColumn { display: "error"}
                    /*rows: [
                        {
                            "ip": "125.30.1.1",
                            "mac": "0xD5D5D5D",
                            "statusUpdata": "normal",
                            "error" :"0x0000"
                        },
                        {
                            "ip": "125.30.10.2",
                            "mac": "0xF5F5F5F5",
                            "statusUpdata": "normal",
                            "error" :"0x0000"
                        }
                    ]*/
                }
                delegate:  DelegateChooser{
                    DelegateChoice{
                        //column:
                        delegate: Rectangle{
                            implicitWidth: 300
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
            id: updateOption
            y: 612
            height: 243
            color: "#00000000"
            border.color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: notiTable.bottom
            anchors.rightMargin: 65
            anchors.leftMargin: 73
            anchors.topMargin: 13

            Rectangle {
                id: selectDevice
                x: 0
                height: 200
                width: parent.width/2
                color: "#00000000"
                border.color: "#00000000"
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.topMargin: 41
                anchors.leftMargin: 0
                ComboBox {
                    id: comboboxId
                    width: parent.width / 2
                    height: 50
                    font.pointSize: 15
                    displayText: "Select IP Devices"
                    model: ListModel {
                        id : comboList
                    }/*{
                        ListElement { name: "One";  ischecked: true }
                        ListElement { name: "Two";  ischecked: false }
                        ListElement { name: "Three"; ischecked: false }
                    }*/

                    delegate: Item {
                        width: parent.width
                        height: 50
                        Row {
                            spacing: 5
                            anchors.fill: parent
                            anchors.margins: 5
                            CheckBox {
                                id: checkboxId
                                height: parent.height
                                width: height
                                checked: ischecked
                                //onPressed: checked = !checked
                                onCheckedChanged: {
                                    if(checked)
                                    {
                                        ischecked = true
                                        listmodelId.append({ "name": name})

                                    }
                                    else if(!checked)
                                    {
                                        ischecked = false
                                        var Index = internal.findIndex(listmodelId,name)
                                        listmodelId.remove(Index,1)
                                    }
                                }
                            }

                            Label {
                                text: name
                                width: parent.width - checkboxId.width
                                height: parent.height
                                verticalAlignment: Qt.AlignVCenter
                                horizontalAlignment: Qt.AlignHCenter
                            }
                        }
                    }
                }
                Rectangle{
                    id : headListitem
                    height: 50
                    color: "#efbfbf"
                    width: parent.width / 2
                    anchors.left: comboboxId.right
                    Label{
                        color: "#202020"
                        text: "Selected IP Device"
                        font.pointSize: 20

                    }
                }
                ListModel {
                    id: listmodelId
                }

                ListView {
                    //id: headListitem
                    width: 200
                    height: 150
                    anchors.left: comboboxId.right
                    anchors.right: parent.right
                    anchors.top: comboboxId.bottom
                    anchors.rightMargin: 0
                    anchors.topMargin: 0
                    clip: true
                    model: listmodelId


                    delegate: Item {
                        height: 50
                        width: 436
                        Rectangle {
                            
                            color: "#FFFFFF"
                            anchors.fill: parent
                            Text {
                                anchors.centerIn: parent
                                text: name
                            }
                        }
                    }

                }
            }

            Rectangle {
                id: typeCheck
                width: 378
                height: 170
                color: "#00000000"
                border.color: "#00000000"
                anchors.left: selectDevice.right
                anchors.top: parent.top
                anchors.topMargin: 0
                anchors.leftMargin: 0

                Rectangle {
                    id: typeHead
                    width: 250
                    height: 45
                    color: "#555555"
                    border.color: "#00000000"
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.leftMargin: 0
                    anchors.topMargin: 0
                    Label {
                        width: 263
                        height: 46
                        color: "#ffffff"
                        text: "Type selection"
                        anchors.left: parent.left
                        font.pointSize: 20
                        anchors.leftMargin: 20
                    }
                }

                CheckBox {
                    id: checkModbus
                    anchors.left: parent.left
                    anchors.top: typeHead.bottom
                    anchors.topMargin: 5
                    anchors.leftMargin: 0
                    onCheckedChanged:{
                        if(checked){
                            checkMQTT.checked = !checked
                            internal.typeConnect ="Modbus"
                        }
                    }
                }

                CheckBox {
                    id: checkMQTT
                    anchors.left: parent.left
                    anchors.top: checkModbus.bottom
                    anchors.leftMargin: 0
                    anchors.topMargin: 8
                    onCheckedChanged:{
                        if(checked){
                            checkModbus.checked = !checked
                            internal.typeConnect ="MQTT"
                        }
                    }
                }

                Label {
                    width: 263
                    height: 46
                    color: "#ffffff"
                    text: "Modbus Protocol"
                    anchors.left: checkModbus.right
                    anchors.top: typeHead.bottom
                    anchors.topMargin: 5
                    anchors.leftMargin: 5
                    font.pointSize: 20

                }

                Label {
                    width: 263
                    height: 46
                    color: "#ffffff"
                    text: "MQTT Protocol"
                    anchors.left: checkMQTT.right
                    anchors.top: typeHead.bottom
                    font.pointSize: 20
                    anchors.leftMargin: 5
                    anchors.topMargin: 51
                }
            }

            Rectangle {
                id: deviceHead
                x: 0
                width: 400
                height: 40
                color: "#555555"
                border.color: "#00000000"
                anchors.top: parent.top
                anchors.topMargin: 0
                Label {
                    width: 263
                    height: 46
                    color: "#ffffff"
                    text: "Device selection section"
                    anchors.left: parent.left
                    font.pointSize: 20
                    anchors.leftMargin: 20
                }
            }
        }
        Connections{
            target: UpdatbackEnd

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

                comboList.append({ "name": ip , "ischecked":false})
            }
            function onSetBoolDeviceClear(state_btn){
                print("clear device done")
                tableView.model.clear()
                comboList.clear()
            }

            function onSetBoolStatClear(state_btn){
                print("clear update done")
                tableStatus.model.clear()
            }

            function onSetContextStatus(ip,date,errorC){
                
                tableStatus.model.appendRow({
                    "ip":ip,
                    "mac":internal.findMac(tableView,ip),
                    "date":date,
                    "error":errorC
                })

            }
            function onSetContexNoti(context){
                contextNoti.text = context
            }
        }
    }
}





/*##^##
Designer {
    D{i:0;formeditorZoom:0.5}
}
##^##*/
