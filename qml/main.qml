import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.0

import "../qml/controls"


Window {
    id: window
    width: 1980
    height: 1080
    minimumWidth: 800
    minimumHeight: 580
    visible: true
    color: "#00000000"
    title: qsTr("DeviceMan")

    flags: Qt.Window | Qt.FramelessWindowHint

    property int windowStatus: 0 //0=Normal() ,1=Maximized()
    property int windowMargin: 10
    property int windowBuffer: 0

    QtObject{
        id:internal
        function changeIcon(){
            if(windowStatus ==1){
                maximize.iconsource = "../icon/restore.png"
            }
            else{
                maximize.iconsource = "../icon/max.png"
            }
        }
        function resetResize(){
            resizeleft.visible = true
            resizeRight.visible = true
            resizeBottom.visible = true
            resizeRB.visible = true
        }

        function maximizeRe(){ //toggle window

            if(windowStatus ==0){
                window.showMaximized()
                windowStatus =1
                windowMargin =0
                resizeleft.visible =false
                resizeRight.visible = false
                resizeBottom.visible = false
                resizeRB.visible = false
            }
            else if(windowStatus ==1){
                window.showNormal()
                windowStatus =0
                windowMargin =10
                internal.resetResize()
            }
            internal.changeIcon()

        }

        function windowRe(){
            if(windowStatus ==0){
                window.showNormal()
                windowStatus =0
                windowMargin =10
                internal.resetResize()
            }
        }

        function miniconfig(){
            window.showMinimized()
            windowStatus =0
            windowMargin =10

        }
    }
    Rectangle {
        id: bg
        width: 990
        height: 570
        color: "#3e4242"
        radius: 3
        border.width: 9
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: windowMargin
        anchors.bottomMargin: windowMargin
        anchors.leftMargin: windowMargin
        anchors.topMargin: windowMargin
        z:1

        Rectangle {
            id: app_content
            color: "#00000000"
            border.color: "#00000000"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.bottomMargin: 0
            anchors.topMargin: 0

            Rectangle {
                id: menubar
                width: 70
                color: "#191919"
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.leftMargin: 0
                anchors.topMargin: 0

                PropertyAnimation{
                    id:animateMenu
                    target: menubar
                    property: "width"
                    to: if(menubar.width ==70) return 250; else return 70
                    duration: 1000
                    easing.type: Easing.InOutQuint
                }

                Column {
                    id: menu
                    width: 70
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    spacing: 12
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    anchors.bottomMargin: 0
                    anchors.topMargin: 37
                    ToggleBtn{
                        width: menubar.width
                        onClicked: animateMenu.running = true

                    }
                    LeftMenuBtn {
                        id: btnHome
                        width: menubar.width
                        text: qsTr("home")
                        onClicked: {
                            update.isActMenu = false
                            btnHome.isActMenu = true
                            stackView.push(Qt.resolvedUrl("../qml/page/home.qml"))
                            backend.refreshmentTable(btnHome.autoRepeat)
                        }

                    }

                    LeftMenuBtn {
                        id: update
                        width: menubar.width
                        text: qsTr("home")
                        isActMenu: false
                        iconsource: "../icon/update_i.png"

                        onClicked: {
                            btnHome.isActMenu = false
                            update.isActMenu = true
                            stackView.push(Qt.resolvedUrl("../qml/page/update.qml"))
                            backend.refreshmentTable(update.autoRepeat)
                            backend.refreshmentStatus(update.autoRepeat)
                        }

                    }
                }
            }

            Rectangle {
                id: topbar
                height: 35
                color: "#191919"
                anchors.left: menubar.right
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.leftMargin: 0
                anchors.rightMargin: 2
                anchors.topMargin: 0

                DragHandler{
                    onActiveChanged: if(active){
                                         window.startSystemMove()
                                         internal.windowRe()
                                     }
                }

                Row {
                    id: icontop
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    spacing: 15
                    anchors.rightMargin: 0
                    anchors.bottomMargin: 0
                    anchors.topMargin: 0

                    MiniBtn{
                        id: minimize
                        iconsource: "../icon/mini.png"
                        colorPressed: "#313030"
                        onClicked: {
                            window.showMinimized()
                            internal.miniconfig()
                        }
                    }

                    MiniBtn {
                        id: maximize
                        colorPressed: "#313030"
                        iconsource: "../icon/max.png"
                        onClicked: {
                            internal.maximizeRe()
                            //internal.reActiveSize()
                        }
                    }

                    MiniBtn {
                        id: btnClose
                        colorMouseOver: "#e41b1b"
                        colorPressed: "#c50f0f"
                        iconsource: "../icon/close.png"
                        onClicked: window.close()
                    }
                }
            }

            Rectangle {
                id: display
                y: 81
                color: "#ffffff"
                border.color: "#00000000"
                anchors.left: menubar.right
                anchors.right: parent.right
                anchors.top: toolbar.bottom
                anchors.bottom: parent.bottom
                clip: true
                anchors.rightMargin: 9
                anchors.leftMargin: 0
                anchors.bottomMargin: 8
                anchors.topMargin: 0
                z:2

                StackView {
                    id: stackView
                    width: display.width
                    height: display.width
                    anchors.fill: parent
                    initialItem: Qt.resolvedUrl("../qml/page/home.qml")
                    
                }
            }

            Rectangle {
                id: toolbar
                height: 75
                color: "#333333"
                border.color: "#00000000"
                anchors.left: menubar.right
                anchors.right: parent.right
                anchors.top: topbar.bottom
                anchors.rightMargin: 9
                anchors.leftMargin: 0
                anchors.topMargin: 0

                Row {
                    id: tool
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    spacing: 7
                    anchors.rightMargin: 0
                    anchors.leftMargin: 37
                    anchors.bottomMargin: 0
                    anchors.topMargin: 21

                    Tools{
                        id: reDevice
                        width: 51
                        height: tool.height
                        iconheight: 22
                        iconWidth: 22
                        checked: true
                        iconsource: "../icon/re-device.svg"
                        
                        onClicked: {
                            backend.refreshmentTable(reDevice.autoRepeat)
                        }

                    }

                    Tools {
                        id: reStatus
                        width: 51
                        height: tool.height
                        actMenuTabL: "#00e1fb"
                        iconWidth: 22
                        iconheight: 22
                        checked: true
                        iconsource: "../icon/refresh-status.png"

                        onClicked: {
                            backend.refreshmentStatus(reStatus.autoRepeat)
                        }
                    }

                    Tools {
                        id: reNoti
                        width: 51
                        height: tool.height
                        actMenuTabL: "#f2fb00"
                        iconWidth: 22
                        iconheight: 22
                        checked: true
                        iconsource: "../icon/refresh-noti.png"

                        onClicked: reNoti.isActBtn = true
                    }
                }

                Rectangle {
                    id: rectangle
                    color: "#2d2d2d"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: tool.top
                    anchors.rightMargin: 0
                    anchors.topMargin: 0
                    anchors.bottomMargin: 0

                    Label {
                        id: titleToolsbar
                        y: 0
                        width: 93
                        height: 21
                        color: "#ffffff"
                        text: qsTr("Toolsbar")
                        anchors.left: parent.left
                        font.pointSize: 10
                        anchors.leftMargin: 9
                        styleColor: "#3c3b3b"
                    }
                }
            }
        }
    }

    DropShadow{
        visible: true
        anchors.fill: bg
        horizontalOffset: 0
        verticalOffset: 0
        radius: 10
        samples: 16
        color: "#5b5b5b"
        source: bg
        clip: false
        transparentBorder: true
        z:0
    }

    MouseArea {
        id: resizeleft
        width: 10
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 10
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        cursorShape: Qt.SizeHorCursor

        DragHandler{
            target: null
            onActiveChanged: if(active){window.startSystemResize(Qt.LeftEdge)}
        }
    }

    MouseArea {
        id: resizeRight
        width: 10
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 10
        cursorShape: Qt.SizeHorCursor
        anchors.bottomMargin: 10
        anchors.topMargin: 10
        DragHandler {
            target: null
            onActiveChanged: if(active){window.startSystemResize(Qt.RightEdge)}
        }
    }

    MouseArea {
        id: resizeBottom
        height: 10
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.leftMargin: 10
        cursorShape: Qt.SizeVerCursor
        anchors.bottomMargin: 10
        anchors.rightMargin: 10
        DragHandler {
            target: null
            onActiveChanged: if(active){window.startSystemResize(Qt.BottomEdge)}
        }
    }

    MouseArea {
        id: resizeRB
        x: 965
        y: 545
        width: 25
        height: 25
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        cursorShape: Qt.SizeFDiagCursor
        anchors.bottomMargin: 10
        anchors.rightMargin: 10
        Image {
            id: image
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            source: "../icon/resize.png"
            sourceSize.height: 17
            sourceSize.width: 17
            fillMode: Image.PreserveAspectFit
            z:3
        }

        DragHandler {
            target: null
            onActiveChanged: if(active){window.startSystemResize(Qt.BottomEdge|Qt.RightEdge)}
        }

    }
    Connections{
        target: backend

    }
}



/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
