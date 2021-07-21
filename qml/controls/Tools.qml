import QtQuick 2.0
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.0

Button{
    id: topTools
    text: qsTr("Refresh Btn")

    property color colorDefault: "#333333"
    property color colorMouseOver: "#6f6f6f"
    property color colorPressed: "#3f3f3f"
    property url iconsource: "../../icon/refresh-device.png"
    property int iconWidth: 18
    property int iconheight: 18
    property color actMenuTabL: "#09fb00"
    property color actMenuTabR: "#202020"
    property bool isActBtn: false
    width: 35
    height: 40

    QtObject{
        id: internal
        property var clkBtn: if(topTools.down){
                                topTools.down? colorPressed : colorDefault
                             }else{
                                topTools.hovered? colorMouseOver : colorDefault
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
            color: actMenuTabL
            width: 3
            visible: isActBtn
        }
        Rectangle{
            anchors{
                top:parent.top
                right: parent.right
                bottom: parent.bottom
            }
            color: actMenuTabR
            width: 5
            visible: isActBtn
        }
    }
    contentItem: Item{
            anchors.fill: parent
            id: content
            width: 40
            height: 35
            Image {
                id: btnicon
                y: 7
                width: 41
                height: 41
                source: iconsource
                anchors.leftMargin: 5
                //sourceSize.width: iconWidth
                //sourceSize.height: iconHeight
                fillMode: Image.PreserveAspectFit
                visible: true
                anchors.left: parent.left
                antialiasing: true
            }
        }

}



/*##^##
Designer {
    D{i:0;height:60;width:51}
}
##^##*/
