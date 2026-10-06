# CMake 骨架：Qt6 + QML 模块（Qt 6 主口径）
# 判据：qt_add_qml_module 一次生成 qmldir、编译 QML、产出插件目标。
cmake_minimum_required(VERSION 3.21)
project(app LANGUAGES CXX)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Qml Quick)
qt_standard_project_setup()

qt_add_executable(app
    main.cpp
    counter.h counter.cpp
)

qt_add_qml_module(app
    URI Org.App
    VERSION 1.0
    QML_FILES Main.qml
    NO_RESOURCE_TARGET_PATH
)

target_link_libraries(app PRIVATE Qt6::Core Qt6::Gui Qt6::Qml Qt6::Quick)

enable_testing()
add_test(NAME smoke COMMAND app -platform offscreen -import)

# 部署（Windows）：windeployqt --qmldir ${CMAKE_SOURCE_DIR} $<TARGET_FILE:app>
# 缺 --qmldir 时 QML 插件不会被收集，部署后白屏。
