# object-model-meta — QObject 对象模型（moc / 信号槽 / 属性系统）

## 判据要点

- `Q_OBJECT` 是元对象系统的开关：声明信号/槽/`Q_PROPERTY`/`Q_ENUM`/`Q_INVOKABLE` 的类**必须**有它，
  否则 moc 不生成 `metaObject()`，`connect` 在运行期静默失败（Qt6 编译期即报错，Qt5 多为运行期）。
- 连接语法优先级：Qt6 函数指针 `connect(a, &A::sig, b, &B::slot)` > Qt5 字符串 `SIGNAL()/SLOT()`。
  字符串语法无重载消歧时须写规范化签名（`void foo(int)` 无空格/默认值/参数名）。
- 属性系统三件套：`Q_PROPERTY(type name READ write NOTIFY)`。`NOTIFY` 缺失 → QML 绑定不更新；
  setter 未做「值未变则不发通知」→ 绑定风暴。Qt6 可用 `BINDABLE` 支持可绑定属性。
- `emit` 只是空宏，真正的跨线程安全来自**连接类型**：`Qt::AutoConnection` 按收发两端线程决定
  Direct/Queued；Queued 要求参数类型已 `Q_DECLARE_METATYPE` + `qRegisterMetaType`。
- 信号可以在析构中被触发但**不要**在析构里 emit：接收方可能已半销毁。断开应在
  `QObject::destroyed` 或显式 `disconnect()` 处做。
- `sender()` 仅在槽执行期间有效，且开销大；用 `QObject::sender()` 做分支是设计气味，改 lambda 捕获。
- 动态属性 `setProperty("x", v)` 走 `QVariant` 哈希表，只用于工具/样式表桥接，热路径禁用。
- 枚举暴露给 QML：Qt6 用 `Q_ENUM`（配合 `QML_ELEMENT`）；Qt5 需 `Q_DECLARE_METATYPE` + 注册。
- PyQt/PySide 注记：Python 侧信号是 `pyqtSignal`/`Signal` 类属性，须在 `__init__` 前于类中声明；
  覆写 C++ 虚函数须调 `super()`，否则事件链断。

## 取证

`python -B scripts/moc_probe.py --dir <proj>`（缺 Q_OBJECT 静态判定）；
`cmake --build build 2>&1 | Select-String "error"` 看 moc 生成物是否参与编译；
运行期用 `obj->metaObject()->className()` 与 `metaObject()->methodCount()` 实证。

## 边界

只裁 Qt 元对象层；C++ 语言级所有权/移动语义转派 `cpp-expert`。
