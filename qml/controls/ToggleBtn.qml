import QtQuick 2.0
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.0

Button{
    id: btntoggle

    property color colorDefault: "#191919"
    property color colorMouseOver: "#4d4c4c"
    property color colorPressed: "#00a1f1"
    property url iconsource: "../../icon/menu.png"
    width: 250

    QtObject{
        id: internal
        property var clkBtn: if(btntoggle.down){
                                btntoggle.down? colorPressed : colorDefault
                             }else{
                                 btntoggle.hovered? colorMouseOver : colorDefault
                             }
    }

    Text {
        id: textMenu
        width: 128
        height: 16
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 75
        font: btntoggle.font
        color: "#ffffff"
        text: "Menubar"
    }
    implicitWidth: 78
    implicitHeight: 60

    background: Rectangle{
        id: bgBtn
        color: internal.clkBtn
        Image {
            id: btnicon
            source: iconsource
            anchors.leftMargin: 26
            width: 25
            height: 25
            fillMode: Image.PreserveAspectFit
            visible: true
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
        }


        ColorOverlay{
            anchors.fill: btnicon
            source: btnicon
            color: "#ffffff"
            antialiasing: false

        }

    }
}


