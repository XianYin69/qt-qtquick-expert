# rendering-performance — 场景图、剖析与异步/惰性加载

## 判据要点

- Qt Quick 的渲染是**场景图**（scene graph）：Item 是节点，属性变化触发节点更新，
  由 render 线程在 vsync 时批量提交。理解这点才知道「为什么 `update()` 不立即画」。
- `QQuickPaintedItem` 走 CPU 光栅再上传纹理，是场景图的**旁路**：能用
  `QSGNode`/`QQuickItem::updatePaintNode()` 就不要 PaintedItem；大量 PaintedItem 是帧率杀手。
- 批处理（batching）：同纹理同着色器的节点会被合批。混用不同纹理/`ShaderEffect` 会打断合批，
  表现为 draw call 上升——须用 QML Profiler 的 render 轨道实证，不得凭感觉说「GPU 瓶颈」。
- `layer.enabled: true` 把子树离屏成纹理：适合静态+多次复用（如阴影），
  对动画中的子树反而每帧重绘离屏目标；`layer.effect` 代价更高。
- 透明与圆角：`opacity` 链过深、逐帧 `antialiasing` 大图、`Gradient` 每帧重建都是常见热点；
  静态视觉改预烘焙贴图（`Image` + `mipmap`）。
- 后端与降级：`QSG_RHI_BACKEND`（direct/opengl/vulkan/metal）、`QT_QUICK_BACKEND=software`
  用于无 GPU 环境；软件后端下 `ShaderEffect` 不可用——判据须写清目标平台。
- 异步与惰性：`Image.asynchronous: true`、`Loader.active` 控制按需创建、
  `ListView.cacheBuffer` 增缓冲换平滑；`fetchMore` 做数据侧惰性。三者解决的是不同瓶颈，别混谈。
- 剖析基线：QML Profiler（loading / animations / behaviors / javascript / pixmaps /
  render / consolidated events 轨道）+ `QT_LOGGING_RULES="qt.scenegraph.time.*=true"`。
  **没有帧时间曲线的优化建议一律标 [本地] 假设**。
- 高 DPI：`devicePixelRatio` 非整数缩放时纹理重采样模糊，位图资源须多倍图或 SVG。

## 取证

`python -B scripts/perf_probe.py --dir <qml>`；`python -B scripts/env_probe.py`；
实测：QML Profiler 导出 + `qt.scenegraph.time.renderloop` 日志取帧间隔分布。

## 边界

着色器/图形管线深层优化超出本技能；须转派专项或先联网取证（浏览器学习）。
