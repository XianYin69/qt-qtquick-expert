// Main.qml — ListView + delegate 骨架
// 判据：delegate 必须假定会被回收复用，业务状态不得存在 delegate 局部属性里。
import QtQuick
import QtQuick.Controls
import Org.App

ApplicationWindow {
    id: win
    width: 360
    height: 480
    visible: true

    Counter {
        id: counter
    }

    ListView {
        anchors.fill: parent
        model: 200                 // 大集合用 ListView，不用 Repeater
        cacheBuffer: 400           // 缓冲换滚动平滑
        delegate: ItemDelegate {
            width: ListView.view.width
            required property int index
            text: "row " + index + " / value " + counter.value
            onClicked: counter.increment()
        }
    }

    // 高 DPI：位图资源给 @2x 或 SVG；字体用 pointSize 不用 pixelSize。
    // 无障碍：自定义 Item 须给 Accessible.role / Accessible.name。
}
