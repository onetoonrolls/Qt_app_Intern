import QtQuick 2.0
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.0

Button{
    id: minimaize

    property color colorDefault: "#191919"
    property color colorMouseOver: "#4d4c4c"
    property color colorPressed: "#000000"
    property url iconsource: "../../icon/mini.png"
    width: 35
    height: 35

    QtObject{
        id: internal
        property var clkBtn: if(minimaize.down){
                                minimaize.down? colorPressed : colorDefault
                             }else{
                                minimaize.hovered? colorMouseOver : colorDefault
                             }
    }
    implicitWidth: 35
    implicitHeight: 35

    background: Rectangle{
        id: bgBtn
        color: internal.clkBtn
        Image {
            id: btnicon
            source: iconsource
            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter
            width: 16
            height: 16
            fillMode: Image.PreserveAspectFit
            visible: false
        }

        ColorOverlay{
            anchors.fill: btnicon
            source: btnicon
            color: "#ffffff"
            antialiasing: false

        }

    }
}





/*##^##
Designer {
    D{i:0;formeditorZoom:16}
}
##^##*/
