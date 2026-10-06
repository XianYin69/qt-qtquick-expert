# dependence（依赖声明）

本技能**不内嵌**其他技能正文；能力一律经声明获取。每行一条 `名称 | 类型 | 来源`，
类型为 skill|software|repo|doc。SMS 安装时对本目录条目与本体做同样检查与净化
（trust 标注·未审/隔离拒装·仓库下载须网络授权）。

```
file_ops             | skill    | local:skill_manage_system
code-guidelines      | skill    | local
pavedpath-code       | skill    | local
ui-design            | skill    | local
database-management  | skill    | local
concurrency-design   | skill    | local
cpp-expert           | skill    | local
python-expert        | skill    | local
python               | software | system
git                  | software | system
cmake                | software | system
qt6                  | software | optional
```

## 用途映射

| 依赖 | 承担能力 | 触发节点 |
|---|---|---|
| file_ops | 联网检索/取页、文件读写（版本行为与 API 取证） | 浏览器学习 · 知识检索 · 经验查询 |
| code-guidelines | 命名/注释/复杂度/评审通用准则 | 专家判断 · 整体审查 |
| pavedpath-code | 已验证实现范式与脚手架 | 重构建议 · 输出交付 |
| ui-design | 视觉/交互专项判断（本技能不自行裁视觉） | 领域定位（转派） |
| database-management | 持久化/查询专项（转派，不内嵌） | 领域定位（转派） |
| concurrency-design | 并发架构设计；本技能只出 Qt 线程模型级取证 | 领域定位（转派） |
| cpp-expert | C++ 语言级判据（所有权/移动/UB） | 专家判断（Qt 层之外的 C++ 问题） |
| python-expert | PyQt/PySide 侧 Python 语言级判据 | 专家判断（绑定层问题） |
| python | 运行 `scripts/` 探针 | 取证探查 · 整体审查 · 收尾 |
| git | 功能分支→dev→main 工作流 | 初始化 · 收尾 |
| cmake | `qt_add_qml_module` / `find_package(Qt6)` 实测 | 取证探查（build_probe） |
| qt6 | `moc` / `qmllint` / `windeployqt` 等工具链 | 取证探查（缺省即降级为静态判据） |

## 边界

- 跨技能只传「意图 + 参数」，由对方在其目录内执行；禁止直接 import 他技能模块。
- 依赖缺失：记 `process_chain interrupt` 并报告缺项，禁止伪造能力继续。
- 增删依赖须走 [update 审批流](../update/update.md) 并记 CHANGELOG；每条必附 `source_url`。
- 自检：`python -B scripts/knowledge_index.py --check-deps`

## 相关

- [deps.json](deps.json) · [薄技能依赖约束](../resistance/薄技能依赖约束/薄技能依赖约束.md)
