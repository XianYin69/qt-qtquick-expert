# 评审清单 · object-model-meta

- [ ] blocking | 声明信号/槽/Q_PROPERTY 的类缺 `Q_OBJECT` | [moc docs]
- [ ] blocking | Queued 连接传未注册类型（缺 `qRegisterMetaType`） | [signalsandslots docs]
- [ ] blocking | 跨 DLL 边界传 `QPrivateSignal` 重载签名不匹配（Qt5 字符串语法） | [moc docs]
- [ ] major | `Q_PROPERTY` 缺 `NOTIFY`，QML 绑定不刷新 | [properties docs]
- [ ] major | setter 不做「同值不通知」导致绑定风暴 | [properties docs]
- [ ] major | Qt5 字符串 `SIGNAL()/SLOT()` 用于重载函数未消歧 | [signalsandslots docs]
- [ ] major | 析构函数中 `emit` 信号 | [signalsandslots docs]
- [ ] minor | 用 `sender()` 做分支而非 lambda 捕获上下文 | [本地]
- [ ] minor | 热路径使用动态属性 `setProperty` | [properties docs]
- [ ] verify | `moc_probe.py --dir <proj>` + 一次真实构建日志
