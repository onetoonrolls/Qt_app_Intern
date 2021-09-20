import QtQuick 2.15
import QtQuick.Controls 2.15
import Qt.labs.qmlmodels 1.0
import QtQuick.Window 2.15

Item {
    width: Screen.desktopAvailableWidth -69
    height: Screen.desktopAvailableHeight -108
    //width: 1821
    //height: 930

    QtObject{
        id: internal
        property string typeConnect: ""
        property bool notiset: false
        function findIndex(myModel,searchedId){
            for(var i = 0; i < myModel.count; i++) {
                var elemCur = myModel.get(i).name;
                if(searchedId == elemCur) {
                    return i
                }
            }
        }

        function formatText(count, modelData) {
            var data = count === 12 ? modelData + 1 : modelData;
            return data.toString().length < 2 ? "0" + data : data;
        }
        
        function getAllitemlist(myModel){
            for(var i = 0; i < myModel.count; i++){
                //print("Item list : ",myModel.get(i).name)
                UpdatbackEnd.getUpdateIP(myModel.get(i).name)
            }
        }

        function unCheckBox(myModel){
            for(var i=0; i< myModel.count;i++){
                myModel.setProperty(i, "ischecked", false)
            }
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
        id: bg
        color: "#202020"
        border.color: "#00000000"
        anchors.fill: parent
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0

        Label {
            id: updatepage
            width: 263
            height: 46
            color: "#ffffff"
            text: qsTr("Update page")
            anchors.left: parent.left
            anchors.top: parent.top
            horizontalAlignment: Text.AlignHCenter
            anchors.topMargin: 0
            anchors.leftMargin: 0
            font.pointSize: 20
        }

        Row {
            id: confirmBtn
            x: 1277
            y: 849
            width: 501
            height: 82
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 30
            anchors.rightMargin: 30
            spacing: 18

            Button {
                id: updateNow
                width: 150
                height: 65
                text: "confirm"
                onClicked: {
                    internal.getAllitemlist(listmodelId)
                    contextNotitext.append({"data":"Processing to python backend"})
                    internal.notiset = true
                    //contextNoti.text = "Processing to python backend"
                    UpdatbackEnd.updateFirmware(internal.typeConnect)
                    //UpdatbackEnd.starCount(true)
                }
            }

            Button {
                id: setTime
                width: 150
                height: 65
                text: "set time"
                onClicked: {
                var hour = hoursTumbler.currentIndex
                var min = minutesTumbler.currentIndex
                var posfix = amPmTumbler.currentIndex
                if(timer.visible){
                    UpdatbackEnd.setTimeupdate(hour,min,posfix)
                }
                else{
                    UpdatbackEnd.setTimeupdate(-1,-1,-1)
                }
            }
            }

            Button {
                width: 150
                height: 65
                id: cancle
                text: "cancle"
                onClicked: {
                    internal.unCheckBox(comboList)
                    UpdatbackEnd.cancleTimer(true)
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
            height: 40
            color: "#7d7d7d"
            border.color: "#00000000"
            anchors.left: nitoUpStatus.right
            anchors.right: parent.right
            anchors.top: deviceTable.bottom
            anchors.rightMargin: 65
            anchors.topMargin: 10
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
            id: verticalHeader
            x: deviceTable.x-30
            y: deviceTable.y
            width: 30
            syncView: tableView
            clip: true
            height: tableView.height
            anchors.right: deviceTable.left
            anchors.top: updatepage.bottom
            anchors.topMargin: 29
            anchors.rightMargin: 0
        }

        HorizontalHeaderView {
            id: horiHeader
            x: deviceTable.x
            width: tableView.width
            syncView: tableView
            clip: true
            height: 30
            anchors.bottom: deviceTable.top
            anchors.bottomMargin: 0
        }

        Rectangle {
            id: deviceTable
            height: 190
            color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: updatepage.bottom
            anchors.rightMargin: 65
            anchors.topMargin: 29
            anchors.leftMargin: 73

            TableView {
                id: tableView
                anchors.fill: parent
                synchronousDrag: false
                pixelAligned: false
                boundsBehavior: Flickable.StopAtBounds
                columnSpacing: 1
                rowSpacing: 1
                clip: true
                syncDirection: Qt.Vertical | Qt.Horizontal

                //TableViewColumn{}

                ScrollBar.vertical: ScrollBar {
                    id: tableVerticalBar
                    height: tableView.height
                    anchors.right: parent.right
                    clip: true
                    anchors.rightMargin: 0
                    active: true
                    //policy:ScrollBar.AlwaysOnS
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
            }
        }

        
        VerticalHeaderView {
            id: statusVerticalHeader
            x: notiTable.x-30
            y: 383
            width: 30
            syncView: tableStatus
            clip: true
            height: tableStatus.height
            anchors.right: notiTable.left
            anchors.rightMargin: 0
        }
        
        HorizontalHeaderView {
            id: statushoriHeader
            x: notiTable.x
            width: tableStatus.width
            syncView: tableStatus
            clip: true
            height: 30
            anchors.bottom: notiTable.top
            anchors.bottomMargin: 0
        }

        Rectangle {
            id: notiTable
            y: notiTable.y
            width: 1264
            height: 180
            color: "#00000000"
            border.color: "#00000000"
            anchors.left: parent.left
            anchors.top: nitoUpStatus.bottom
            anchors.leftMargin: 73
            anchors.topMargin: 40
            
            TableView {
                id: tableStatus
                anchors.fill: parent
                contentWidth: 900
                synchronousDrag: false
                pixelAligned: false
                boundsBehavior: Flickable.StopAtBounds
                columnSpacing: 1
                rowSpacing: 1
                clip: true
                syncDirection: Qt.Vertical | Qt.Horizontal

                ScrollBar.vertical: ScrollBar {
                    id: tablestatusVerticalBar
                    x: 1200
                    height: tableStatus.height
                    anchors.right: parent.right
                    clip: true
                    anchors.rightMargin: 0
                    active: true
                    //policy:ScrollBar.AlwaysOnS
                }

                model: StatusModel

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
            width: 1500
            height: 154
            color: "#00000000"
            border.color: "#00000000"
            anchors.left: parent.left
            anchors.top: notiTable.bottom
            anchors.leftMargin: 73
            anchors.topMargin: 13

            Rectangle {
                id: selectDevice
                x: 0
                width: 425
                height: 200
                color: "#00000000"
                border.color: "#00000000"
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.topMargin: 41
                anchors.leftMargin: 0
                ComboBox {
                    id: comboboxId
                    width: 421
                    height: 50
                    font.pointSize: 15
                    displayText: "Select IP Devices"
                    model: ListModel {
                        id : comboList
                    }

                    delegate: Item {
                        width: 100
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
                ListModel {
                    id: listmodelId
                    Component.onCompleted :{
                        UpdatbackEnd.appendToListCheck(true)

                    }
                }

                ListView {
                    //id: headListitem
                    width: 200
                    height: 150
                    visible: false
                    anchors.top: comboboxId.bottom
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
                width: 301
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
                    y: 0
                    width: 372
                    height: 46
                    color: "#ffffff"
                    text: "Device selection section"
                    anchors.left: parent.left
                    font.pointSize: 20
                    anchors.leftMargin: 20
                }
            }

            Rectangle {
                id: timeUpdate
                x: 828
                y: 0
                width: 400
                height: 200
                color: "#00000000"
                border.color: "#00000000"
                anchors.left: typeCheck.right
                anchors.top: parent.top
                anchors.leftMargin: 0
                anchors.topMargin: 0

                Rectangle {
                    id: timerhead
                    x: 0
                    y: 0
                    width: 400
                    height: 40
                    color: "#555555"
                    border.color: "#00000000"
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.leftMargin: 0
                    anchors.topMargin: 0
                    Label {
                        y: -3
                        width: 270
                        height: 46
                        color: "#ffffff"
                        text: "Set update timer"
                        anchors.left: checktimer.right
                        font.pointSize: 20
                        anchors.leftMargin: 20
                    }

                    CheckBox {
                        id: checktimer
                        anchors.left: parent.left
                        anchors.top: parent.top
                        checked: false
                        anchors.leftMargin: 5
                        anchors.topMargin: 0
                        onCheckedChanged: {
                                    if(checked)
                                    {
                                        timer.visible = true
                                    }
                                    else if(!checked)
                                    {
                                        timer.visible = false

                                    }
                                }
                    }
                }

                Component {
                    id: delegateComponent

                    Label {
                            text: internal.formatText(Tumbler.tumbler.count, modelData)
                            opacity: 1.0 - Math.abs(Tumbler.displacement) / (Tumbler.tumbler.visibleItemCount / 2)
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                            font.pixelSize: fontMetrics.font.pixelSize * 2.3
                            color: "#ffffff"
                    }
                }

                FontMetrics {
                    id: fontMetrics
                }

                Rectangle {
                    id: timer
                    width: 250
                    height: 152
                    visible : false
                    color: "#00000000"
                    border.color: "#00000000"
                    anchors.left: parent.left
                    anchors.top: timerhead.bottom
                    anchors.leftMargin: 0
                    anchors.topMargin: 0

                    Frame {
                        id: frame
                        width: 250
                        height: 152
                        padding: 0
                    }

                    Row {
                        id: row
                        width: frame.width
                        height: 150
                        spacing: 10

                        Tumbler {
                            id: hoursTumbler
                            width: frame.width/3.5
                            height: row.height
                            clip: true
                            model: 12
                            delegate: delegateComponent
                        }

                        Tumbler {
                            id: minutesTumbler
                            width: frame.width/3.5
                            height: row.height
                            clip: true
                            model: 60
                            delegate: delegateComponent
                            
                            }

                        Tumbler {
                            id: amPmTumbler
                            width: frame.width/3.5
                            height: row.height
                            clip: true
                            model: ["AM", "PM"]
                            delegate: delegateComponent
                        }
                    }
                } 
            }
        }
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
        target: UpdatbackEnd

        function onSetContextListcheck(ip){
            comboList.append({ "name": ip , "ischecked":false})
        }
        
        function onSetClearListcheck(bool){
            comboList.clear()
        }

        function onSetContexNoti(context){
            contextNotitext.append({"data": context})
            internal.notiset = true
            //contextNoti.text = context
        }
    }
    //Component.onCompleted: console.log("update page created ")
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.5}D{i:60}
}
##^##*/
