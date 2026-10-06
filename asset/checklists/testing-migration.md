# 评审清单 · testing-migration

- [ ] blocking | 声称「已迁移/测试通过」但无 `ctest` 实跑输出 | [portingguide]
- [ ] blocking | queued 信号立即断言（未 `QSignalSpy::wait`）→ 竞态假绿/假红 | [qtest docs]
- [ ] blocking | 仍用 Qt6 已移除项（`QRegExp`/`QDesktopWidget`/`QTextCodec`） | [portingguide]
- [ ] major | `QVector` 迁移后未复核迭代器失效与 `resize` 语义 | [portingguide]
- [ ] major | GUI 测试用 `QTEST_MAIN` 但无 `when: windowShown`（QML 侧） | [本地]
- [ ] major | 模型改动未挂 `QAbstractItemModelTester` | [qabstractitemmodeltester docs]
- [ ] major | 一次性全量迁移（未按模块切基线） | [portingguide]
- [ ] minor | 用 `QTest::qWait` 代替结构性等待 | [qtest docs]
- [ ] minor | PyQt6 窄化枚举未改（`Qt.AlignLeft` 直用） | [qtforpython docs]
- [ ] verify | `migration_probe.py` + `qml_lint.py` + `ctest --output-on-failure`
