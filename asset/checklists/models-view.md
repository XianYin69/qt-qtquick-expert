# 评审清单 · models-view

- [ ] blocking | 改了数据未调 `begin/endInsert|Remove|ChangeRows`（视图不更新/崩溃） | [model docs]
- [ ] blocking | `createIndex` 内部指针指向临时对象（悬垂） | [model docs]
- [ ] blocking | 跨源模型与代理模型混用 `QModelIndex` | [qsortfilterproxymodel docs]
- [ ] major | QML 取不到值：未覆写 `roleNames()` | [model docs]
- [ ] major | 大列表用 `Repeater` 而非 `ListView` | [qml docs]
- [ ] major | 频繁 `layoutChanged`/`resetModel` 代替局部 `dataChanged` | [model docs]
- [ ] major | 百万级用 `QStandardItemModel` | [qstandarditemmodel docs]
- [ ] minor | delegate `sizeHint` 逐行变化（滚动条跳动、复用失效） | [qabstractitemmodel docs]
- [ ] minor | 未实现 `canFetchMore/fetchMore` 却声称惰性加载 | [model docs]
- [ ] verify | `QAbstractItemModelTester` 实跑 + `perf_probe.py` 输出
