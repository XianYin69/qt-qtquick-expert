# build-deploy — CMake / qmake / 资源 / 打包 / 许可

## 判据要点

- Qt6 官方构建系统是 **CMake**：`find_package(Qt6 REQUIRED COMPONENTS Core Quick Widgets)` +
  `qt_standard_project_setup()` + `qt_add_executable` + `target_link_libraries(t PRIVATE Qt6::Quick)`。
  qmake 在 Qt 6.9 起标记为弃用路线，新项目不得以 qmake 为权威构建。
- `qt_add_qml_module(TARGET t URI Org.App VERSION 1.0 QML_FILES ... RESOURCES ...)`
  一次搞定三件事：生成 `qmldir`、编译 QML 进资源、产出插件目标。
  手写 `qrc` + `qmlRegisterType` 是 Qt5 形态，Qt6 应改走模块（判据：CMake 手册）。
- 常见坑：`NO_PLUGIN` 与 `PLUGIN_TARGET` 语义相反（前者不产插件、后者指定插件目标）；
  静态链接 Quick 时忘 `Q_IMPORT_QML_PLUGIN`/`QML_IMPORT_PATH` → 运行期 `module not found`。
- 资源：`qrc` 路径大小写敏感（Windows 上开发正常、Linux 部署即坏）；
  大二进制资源别塞 qrc，走文件系统 + `QStandardPaths`。
- 打包：Windows `windeployqt --qmldir <src> <exe>`（干跑用 `--dry-run` 核对插件集）；
  macOS `macdeployqt` 产 bundle 并签名；Android `androiddeployqt` + Gradle（须 `android/` 模板）；
  iOS 走 CMake toolchain。缺 `--qmldir` 时 QML 插件不会被收集——这是最常见的「本机好好的」事故。
- LGPL vs 商业：LGPL 动态链接可闭源，但须允许用户替换 Qt 库（不可静态并入主程序），
  并保留版权声明；静态链接、修改 Qt 源码、或不便替换的场景须商业授权。判据以 qt.io/licensing 为准。
- 可复现性：Qt 版本、模块组件、`CMAKE_PREFIX_PATH`/`Qt6_DIR` 写进 `CMakePresets.json`；
  不靠开发者本机环境变量。
- PyQt/PySide 注记：PySide6 用 `pyside6-project`/`shiboken` 构建，打包走 `PyInstaller` +
  手动收集 `qml/` 插件；`windeployqt` 对 Python 应用无效。

## 取证

`python -B scripts/build_probe.py --dir <proj>`；`python -B scripts/deploy_probe.py --target <exe> --qmldir <dir>`；
实跑 `cmake -S . -B build && cmake --build build` 才算验证。

## 边界

CI/制品仓库与签名证书管理不在本叶；须先联网取证再答。
