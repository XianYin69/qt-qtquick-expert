# 评审清单 · qtquick-qml

- [ ] blocking | 命令式赋值打断属性绑定（含 `onCompleted` 内赋值） | [qml docs]
- [ ] blocking | delegate 把业务状态存在局部属性（复用串数据） | [qml docs]
- [ ] blocking | `createObject` 未指定 parent（对象无人持有/泄漏） | [qml docs]
- [ ] major | 对外属性未标 `required`（缺值静默 undefined） | [qml docs]
- [ ] major | Qt6 项目仍用 `qmlRegisterType` 而未走 `QML_ELEMENT`+模块 | [definetypes docs]
- [ ] major | `Behavior` 与 `Transition` 对同一属性重复定义 | [qml docs]
- [ ] major | delegate 内属性名与外层作用域冲突未加 `id` 前缀 | [qml docs]
- [ ] minor | 大段命令式 JS 写在 QML（应下沉 C++ 或独立 `.js`） | [本地]
- [ ] minor | 未用 `Loader` 而常驻隐藏整块子树 | [qml docs]
- [ ] verify | `qml_lint.py --dir <qml>` 输出（qmllint rc 或 [本地] 疑点）
