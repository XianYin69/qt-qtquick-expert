# scripts（脚本库）

全部英文名、薄实现：只取证与组装，不做判断替代；禁裸 `except`、禁 `print` 调试残留、
禁 >100 字符长行。脚本不限行数，但按职责拆分。缓存一律落用户缓存目录，不写 skill 目录。

## 分类与检索

| 脚本 | 作用 | 典型调用 |
|---|---|---|
| classify_topic.py | 问题 → 知识树叶（关键词打分） | `--tree asset/knowledge_tree.json "<问题>"` |
| knowledge_index.py | 叶索引 / 叶详情 / 依赖清单自检 | `--leaf build-deploy` · `--check-deps` |
| review_checklist.py | 输出评审清单并按 blocking/major/minor 计数 | `--leaf qtquick-qml` |
| advice_compose.py | 组装交付五段（结论/依据/取证/边界/未覆盖） | `--leaf widgets-ui --verdict "..."` |
| check_links.py | 悬空链接校验（红线：必须为 0） | `--root .` |

## 探针

| 脚本 | 探测对象 | 缺工具时 |
|---|---|---|
| env_probe.py | qmake/Qt6 CMake 包/windeployqt/qmllint/PySide6/PyQt6 | 降级为静态判据并标 [本地] |
| moc_probe.py | 信号/槽/属性缺 `Q_OBJECT`、Q_OBJECT 落在 .cpp | 纯静态，无需 Qt |
| qml_lint.py | 优先跑 `qmllint`，否则静态疑点扫描 | 输出 [本地] 疑点清单 |
| build_probe.py | `qt_add_qml_module`、AUTOMOC、链接可见性、qmake 遗留 | 纯静态 |
| deploy_probe.py | `windeployqt --dry-run` / `macdeployqt` 与常见缺项 | 给静态部署清单 |
| perf_probe.py | 场景图不友好写法（layer.effect/Repeater/Timer 0ms） | 纯静态，须 QML Profiler 实测 |
| migration_probe.py | Qt5→Qt6 移除项（QRegExp/QDesktopWidget/quickcontrols2） | 纯静态 |

## 约定

- 退出码：0 通过；1 有疑点/不合格；2 参数错；3 工具缺失（降级）。
- 任何「已验证」字样必须来自本目录脚本的真实运行输出，未运行不得写。
- 新增脚本须同步本文件、`SKILL.md` 可用工具段与 `asset/knowledge_tree.json` 的 `probes`。

## 相关

- [流程总览](../branch/流程/流程.md) · [审查约束](../resistance/审查约束/审查约束.md)
