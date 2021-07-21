import QtQuick 2.0
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.0

Button{
    id: leftmenu
    text: qsTr("Left Menu Text")

    property color colorDefault: "#191919"
    property color colorMouseOver: "#4d4c4c"
    property color colorPressed: "#00a1f1"
    property url iconsource: "../../icon/home.png"
    property int iconWidth: 30
    property int iconheight: 30
    property color actMenu: "#55aaff"
    property color actMenuRigth: "#2c313c"
    property bool isActMenu: true

    QtObject{
        id: internal
        property var clkBtn: if(leftmenu.down){
                                leftmenu.down? colorPressed : colorDefault
                             }else{
                                leftmenu.hovered? colorMouseOver : colorDefault
                             }
    }
    implicitWidth: 250
    implicitHeight: 60

    background: Rectangle{
        id: bgBtn
        color: internal.clkBtn

        Rectangle{
            anchors{
                top:parent.top
                left: parent.left
                bottom: parent.bottom
            }
            color: actMenu
            width: 3
            visible: isActMenu
        }
        Rectangle{
            anchors{
                top:parent.top
                right: parent.right
                bottom: parent.bottom
            }
            color: actMenuRigth
            width: 5
            visible: isActMenu
        }
    }
    contentItem: Item{
            anchors.fill: parent
            id: content
            Image {
                id: btnicon
                anchors.leftMargin: 22
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                source: iconsource
                //sourceSize.width: iconWidth
                //sourceSize.height: iconHeight
                width: iconWidth
                height: iconheight
                fillMode: Image.PreserveAspectFit
                visible: false
                antialiasing: true
            }


            ColorOverlay{
                x: 50
                anchors.fill: btnicon
                source: btnicon
                anchors.verticalCenterOffset: -1
                color: "#ffffff"
                anchors.verticalCenter: parent.verticalCenter
                antialiasing: true
                width: iconWidth
                height: iconheight
            }

            Text{
                color: "#ffffff"
                text: leftmenu.text
                font: leftmenu.font
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 75
            }
        }

}



/*##^##
Designer {
    D{i:0;formeditorZoom:3}
}
##^##*/
