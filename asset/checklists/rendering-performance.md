# 评审清单 · rendering-performance

- [ ] blocking | 无帧时间曲线即断言「更快 / GPU 瓶颈」 | [scenegraph docs]
- [ ] blocking | 大量 `QQuickPaintedItem` 承担主视觉 | [scenegraph docs]
- [ ] major | 动画中的子树开 `layer.enabled`/`layer.effect`（每帧离屏） | [qml docs]
- [ ] major | 混用多纹理/`ShaderEffect` 打断合批且未测 draw call | [scenegraph docs]
- [ ] major | 大图逐帧 `Gradient` / 深 `opacity` 链 | [本地]
- [ ] major | 目标平台未定就推荐后端（software 下 ShaderEffect 不可用） | [本地]
- [ ] minor | 位图资源无多倍图（高 DPI 模糊） | [highdpi docs]
- [ ] minor | 未用 `Image.asynchronous` / `Loader.active` 做首屏惰性 | [qml docs]
- [ ] verify | `perf_probe.py` + QML Profiler 帧间隔曲线（须附实测数值）
