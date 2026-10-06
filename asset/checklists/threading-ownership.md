# 评审清单 · threading-ownership

- [ ] blocking | 非所属线程访问 `QWidget`/`QQuickItem` | [threads docs]
- [ ] blocking | `moveToThread` 的对象带 parent（parent 线程决定子线程） | [threads docs]
- [ ] blocking | `QObject` 同时被 parent 树与智能指针管理（双删） | [qobject docs]
- [ ] blocking | GUI 线程槽内做阻塞 IO / `sleep` | [threads docs]
- [ ] major | Queued 连接参数类型未注册 | [signalsandslots docs]
- [ ] major | 依赖 `deleteLater()` 但线程随即退出且未清 DeferredDelete | [qobject docs]
- [ ] major | `QTimer` 的 parent 与目标 worker 线程不一致 | [threads docs]
- [ ] minor | 用裸指针缓存可能先销毁的 QObject（应 `QPointer`） | [qpointer docs]
- [ ] verify | `env_probe.py` + TSan 实跑；线程断言打点输出
