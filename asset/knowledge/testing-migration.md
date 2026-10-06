# testing-migration — Qt Test、QML TestCase 与 Qt5→Qt6 迁移坑

## 判据要点

- C++ 单测：`Qt::Test` 模块 + `QTEST_MAIN(Class)`/`QTEST_APPLESS_MAIN`（不需 GUI 就别起 app）；
  数据驱动用 `_data()` 配套函数 + `QTest::addColumn`/`QTest::newRow`。
- 信号断言：`QSignalSpy`（Qt6 支持 `wait`/`count`/`at`）；跨线程 queued 信号须
  `QTRY_VERIFY`/`spy.wait()` 而非立即断言，否则竞态假失败。
- 异步断言：`QTest::qWait` 只用于时间相关；结构性等待用 `QSignalSpy::wait` 或
  `qWaitFor`（Qt5）/`QTest::qWaitFor`（Qt6 移除，改 `std::optional` 轮询）——版本差异须写明。
- QML 测试：`import QtTest` + `TestCase` 组件，`target` 指向被测 Item；
  `when: windowShown` 保证窗口可见后再跑；交互用 `MouseArea`/`touch` 系列函数。
  CMake 侧 `qt_add_test(...)` + `qt_add_qml_module(... NO_PLUGIN)` 组合。
- 模型改动必挂 `QAbstractItemModelTester`；委托/视图行为用 `QTest::mouseClick` + 索引断言。
- Qt5→Qt6 高频坑（判据以 porting guide 为准）：`QRegExp`→`QRegularExpression`；
  `QStringRef`→`QStringView`；`QDesktopWidget` 移除→`QScreen`；`QVector` 变 `std::vector` 别名
  （`resize`/迭代器失效语义须复核）；`QVariant::type()`→`typeId()`；`QTextCodec` 移出 Core；
  枚举由 `Qt::Alignment` 位域改 `QFlag` 组合；`quickcontrols2` 模块并入 `quick`；
  高 DPI 默认开启（旧 `AA_EnableHighDpiScaling` 属性移除）。
- 绑定层迁移：PyQt5→PyQt6 枚举改为窄化（`Qt.AlignLeft`→`Qt.AlignmentFlag.AlignLeft`）；
  PySide2→PySide6 模块名 `QtCore` 路径不变但 `shiboken` 版本须与 Qt 对齐。
- 迁移不得「一次改完再测」：按模块切分（先 Core 再 Gui 再 Widgets/Quick），每步留可运行基线。

## 取证

`python -B scripts/migration_probe.py --dir <proj>`；`python -B scripts/qml_lint.py --dir <tst>`；
实跑 `ctest --output-on-failure` 才算「测试通过」。

## 边界

CI 编排与覆盖率门禁策略不在本叶；Python 语言级问题转派 `python-expert`。
