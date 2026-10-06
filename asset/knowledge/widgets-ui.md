# widgets-ui — Widgets：布局、事件、绘制与样式

## 判据要点

- 布局用 `QLayout` 家族，**不要**手摆绝对坐标：`addWidget` 后控件 parent 自动改为布局父件，
  手动 `setParent` 会脱离布局管理。嵌套优先于自定义 `QLayout` 子类。
- `QSizePolicy` 是布局的唯一契约：`Minimum/Preferred/Fixed/Expanding/Ignored` 的
  horizontal×vertical 组合决定拉伸分配；`setMinimumWidth` 与 `sizeHint` 冲突时以约束为准。
- 拉伸靠 `addStretch` / `setStretchFactor` / `QGridLayout` 的 row/column stretch，
  三者语义不同：`setStretchFactor` 只作用于布局内 item，不作用于顶层窗口。
- 事件过滤：`installEventFilter` 的过滤器**必须比被过滤对象先存在**，且过滤器收到的事件
  返回 `true` 即吞掉；重写 `event()` 与 `eventFilter` 混用会让同一事件被处理两次。
- 绘制：只在 `paintEvent` 内建 `QPainter`；`repaint()` 立即重绘（阻塞），常规更新用
  `update()`（合并请求）。热路径禁在 `paintEvent` 里 `new`/加载资源/解析 SVG——预生成 `QPixmap`。
- 坐标：Qt6 全面 `qreal` 化（`QRectF`/`QPointF`），整数 `QRect` 与浮点混用会静默截断；
  高 DPI 下须用 `devicePixelRatio` 标注 `QPixmap`，否则位图模糊。
- 样式：`QStyle`（平台原生观感）与 QSS（`setStyleSheet`）是两套机制。QSS 选择器代价随控件数上升，
  且部分属性（`padding`/`margin`）会改变 sizeHint 导致布局抖动；跨平台外观一致性优先用 `QProxyStyle`。
- 字体与图标：`QFont` 用逻辑点（pointSize），像素字号（pixelSize）在高 DPI 下不缩放；
  图标走 `QIcon` 多尺寸 + SVG，别塞单张 PNG。
- Qt5 遗留注记：`QApplication::setAttribute(Qt::AA_EnableHighDpiScaling)` 在 Qt6 默认开启，
  Qt6 改 `QGuiApplication::setHighDpiScaleFactorRoundingPolicy()`（须在创建 app 前）。

## 取证

`python -B scripts/perf_probe.py --dir <proj>`；`build_probe.py` 查 `QT += widgets`；
实测：`QT_LOGGING_RULES` + 打开 `QWIDGETS` 类别看布局警告；重绘次数用 `paintEvent` 计数打点。

## 边界

视觉/交互设计判断转派 `ui-design`；本叶只裁 Widgets 框架机制。
