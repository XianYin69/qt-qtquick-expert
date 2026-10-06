# 评审清单 · widgets-ui

- [ ] blocking | 在 `paintEvent` 之外构造 `QPainter` 作用于控件 | [本地]
- [ ] blocking | 热路径 `repaint()` 代替 `update()` | [qwidget docs]
- [ ] blocking | `installEventFilter` 返回 true 吞掉必需事件（含 resize） | [events docs]
- [ ] major | 绝对坐标摆控件、未用 `QLayout` | [layout docs]
- [ ] major | `QSizePolicy` 与 `setMinimum*` 冲突致布局抖动 | [qsizepolicy docs]
- [ ] major | `setStretchFactor` 用在顶层窗口（无效） | [qlayout docs]
- [ ] major | `QPixmap` 未标 `setDevicePixelRatio`（高 DPI 模糊） | [highdpi docs]
- [ ] minor | 大范围 QSS 选择器（性能与跨平台观感风险） | [stylesheet docs]
- [ ] minor | 用 `pixelSize` 字体（不随 DPI 缩放） | [qfont docs]
- [ ] verify | `perf_probe.py` + 一次重绘计数打点输出
