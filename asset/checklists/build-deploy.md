# 评审清单 · build-deploy

- [ ] blocking | 新 Qt6 项目以 qmake 为权威构建（qmake 已入弃用路线） | [qmake docs]
- [ ] blocking | `windeployqt` 未带 `--qmldir`（QML 插件缺失，部署即白屏） | [windows-deployment docs]
- [ ] blocking | LGPL 动态链接承诺不成立（静态并入且不允许替换 Qt） | [qt.io/licensing]
- [ ] major | 手写 `qrc`+`qmlRegisterType` 而不用 `qt_add_qml_module` | [cmake-manual]
- [ ] major | `NO_PLUGIN`/`PLUGIN_TARGET` 用反 | [cmake-manual]
- [ ] major | qrc 路径大小写混用（Linux 部署失败） | [resources docs]
- [ ] major | 构建依赖本机环境变量（未写 `CMakePresets`/`Qt6_DIR`） | [本地]
- [ ] minor | 大二进制塞进 qrc（应走文件系统） | [resources docs]
- [ ] minor | 对 PySide6 应用调 `windeployqt` | [qtforpython docs]
- [ ] verify | `build_probe.py` + `deploy_probe.py --dry-run` + 一次真实构建
