# qtquick-qml — QML 语法、类型注册、委托与状态

## 判据要点

- 属性绑定 vs 命令式赋值：`width: parent.width * 0.5` 是绑定；一旦写
  `item.width = 100`（含 `Component.onCompleted` 里赋值）**绑定即被永久打断**。
  需要动态改值就改源属性或用 `Binding` 对象。
- 类型注册三选一，别混：Qt6 首选 `QML_ELEMENT`（配合 `qt_add_qml_module`，自动进模块）；
  不可实例化但需访问枚举/单例用 `QML_UNCREATABLE("原因")`；旧式 `qmlRegisterType` 仅在
  无 CMake 模块或需运行时版本映射时用。Qt5 无 `QML_ELEMENT`，只能 `qmlRegisterType`。
- `required property`（Qt 6.0+）让缺失属性在**加载期**报错，替代静默 `undefined`；
  对外组件应把外部输入项全标 required。
- 委托（delegate）必须假定**可被回收复用**：不能把状态存在 delegate 的局部属性里当业务状态，
  滚动复用会串数据；业务状态一律回指 model 索引或外部 store。
- `states` 只描述「差异集合」，`State { when: ... }` 比 `state: "x"` 命令式切换更可组合；
  `transitions` 匹配的是属性变化，未写 transition 的属性变化是瞬变（不是动画）。
- `Behavior on x {}` 与 `Transition` 会叠加：同一属性两处都定义时，状态切换期间行为不可预期。
- `Loader` 用于按需创建（`active: false` 即销毁实例）；`Component` + `createObject` 用于动态创建，
  须显式给 parent，否则对象无父、由 JS 引擎持有 → 生命周期失控。
- 单例：`QML_SINGLETON` + `pragma Singleton`（目录需 `qmldir` 声明 `singleton`）。
- 作用域陷阱：delegate 内 `modelData`/`index` 与外层同名属性冲突时，就近解析；
  显式 `id` 前缀访问可避免歧义。
- PyQt/PySide 注记：`QmlElement` 装饰器（PySide6 6.4+）等价 `QML_ELEMENT`；
  Python 类属性信号在 QML 侧可直接连；GIL 使 QML 回调仍在 GUI 线程，重计算须下沉线程。

## 取证

`python -B scripts/qml_lint.py --dir <qml>`（有 qmllint 则以其输出为准）；
`QQmlApplicationEngine::load` 返回空对象即加载失败，须打印 `warnings`；
打断绑定用 `QML_DEBUG`/Profiler 的 binding 视图实证。

## 边界

视觉与交互规范转派 `ui-design`；C++ 侧模板/所有权问题转派 `cpp-expert`。
