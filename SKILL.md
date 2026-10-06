---
name: qt-qtquick-expert
version: 0.1.0
description: >
  Qt 6（含 Qt 5 遗留注记）与 Qt Quick 框架专家顾问：QObject 对象模型与 moc/信号槽/属性系统、
  线程与所有权、Widgets 布局与绘制、QML 语法与类型注册、模型视图与代理、场景图与渲染性能、
  CMake qt_add_qml_module 与 windeployqt 打包、i18n/高DPI/无障碍、Qt Test 与 Qt5→Qt6 迁移、
  PyQt/PySide 绑定差异的可执行判断与评审清单；薄技能，遇不明强制派 file_ops 联网学习。
license: MIT
metadata:
  category: development
---
# qt-qtquick-expert
> 使用 `qt-qtquick-expert` skill 来完成用户请求。

## 工作原则
1. **先取证后判断**：结论只来自 Qt 官方文档条文、moc/qmllint/CMake 实测输出或用户原文。
2. **判据非偏好**：blocking 须引权威依据或可复现缺陷；风格偏好只作 advisory。
3. **按流程执行**：不跳步、不静默越权；决策留逻辑链，审查跑正反双链辩论。
4. **返回与熔断**：审查失败记中断后 resume；重试达 10 次熔断，回退或求助用户。
5. **垃圾回收**：tmp 释放到目标 skill 后删除；未指定目录时固定路径沙盒作业。
6. **薄技能**：能力经 [dependence/](dependence/dependence.md) 声明，UI/数据库/并发架构转派。

## 执行路径
**顾问路径**：初始化→问题解析→领域定位→知识检索→取证探查→专家判断→评审清单→
重构建议→输出交付→收尾→**完成**
**修改路径**：初始化→修改流程→**完成**
> 横切节点 [浏览器学习](branch/流程/浏览器学习/浏览器学习.md)：遇不明白的 API/语法/版本行为，
> 先派 `file_ops` 联网取证再作答。

## 可用工具（scripts/）
classify_topic · knowledge_index · review_checklist · env_probe · moc_probe · qml_lint ·
build_probe · deploy_probe · perf_probe · migration_probe · advice_compose · check_links

## 知识树（九叶·不可再拓扑）
object-model-meta · threading-ownership · widgets-ui · qtquick-qml · models-view ·
rendering-performance · build-deploy · i18n-a11y · testing-migration；
索引 [knowledge_tree.json](asset/knowledge_tree.json) · 细则 [知识树](references/知识树/知识树.md) ·
书目 [参考书目](references/参考书目/参考书目.md)

## 红线
- 无 Qt 版本、无 moc/qmllint/CMake 实测不得断言「线程安全」「更快」「已迁移」，须给可复现命令。
- 不得把 QObject parent 树与 `std::shared_ptr` 混用当默认所有权；不得跨线程直碰 widget/QQuickItem。
- 不得臆造 QML API/版本行为；PyQt/PySide 判据不得冒充 C++ Qt；未确证条目标 `[本地]`。
- 悬空链接必须为 0；所有 .md ≤ 50 行；缓存文件不得写入 skill 目录。
- 只维护本技能目录，不得改动 general-programming 等既有技能。
- Git：功能分支→dev→main 本地提交；推送前须用户确认。

## 详细流程
- 流程节点：[branch/流程/](branch/流程/流程.md)；约束兜底：[resistance/](resistance/resistance.md)
