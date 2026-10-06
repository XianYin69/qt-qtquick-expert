# models-view — 模型视图：QAbstractItemModel、代理与 ListView/Repeater

## 判据要点

- 自定义模型三问：**行数从哪来**（`rowCount`）、**数据从哪来**（`data`）、
  **变化怎么通知**（`begin/endInsert|Remove|ChangeRows`）。缺通知 → 视图不更新或崩溃。
- `index()`/`parent()` 必须与 `createIndex` 配对且内部指针稳定；把临时对象指针塞进
  `QModelIndex` 内部指针是悬垂崩溃的头号来源。
- 角色：`roleNames()` 只在 `QAbstractListModel`/自定义模型暴露给 QML 时需要；
  Qt6 可用 `QML_NAMED_ELEMENT` + `QHash<int, QByteArray>` 覆写。缺 roleNames → QML 里取不到值。
- 结构变化必须成对调用 begin/end；`layoutChanged()`/`beginResetModel` 是**重排全表**，
  代价高，能用 `dataChanged` 局部刷新就不要 reset。
- 代理模型：`QSortFilterProxyModel` 的索引与源模型不同——**永远不要跨模型混用 QModelIndex**；
  取源索引用 `mapToSource`。`filterFixedColumn`/`filterKeyColumn` 设 -1 表示全列匹配。
- 大模型：`canFetchMore`/`fetchMore` 实现按需取数；`QListView` 的 delegate 复用要求
  `sizeHint` 稳定，逐行动态高度会让滚动条跳动并破坏复用。
- QML 侧：`ListView` 走 delegate 回收（有 `cacheBuffer`）；`Repeater` **全部实例化**，
  只适合小集合。数据量大却用 Repeater 是典型误选。
- `QStandardItemModel` 便于原型，但每 item 一个堆对象，百万级不可用；生产改自定义模型或
  `QSqlQueryModel`/`QQmlListModel`（后者仅 QML 内可用）。
- 测试：`QAbstractItemModelTester`（Qt Test）可自动校验模型契约，是模型改动的第一道闸。
- PyQt/PySide 注记：Python 侧实现的模型被 C++ 持有，须保持 Python 引用否则包装对象先亡。

## 取证

`python -B scripts/perf_probe.py --dir <proj>`；模型契约用 `QAbstractItemModelTester` 跑一遍；
`ListView` 复用效果看 QML Profiler 的 delegate 创建次数。

## 边界

数据源与查询优化转派 `database-management`；本叶只裁模型视图框架契约。
