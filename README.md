# qt-qtquick-expert

Qt 6（含 Qt 5 遗留注记）与 Qt Quick 框架的**薄顾问技能**：只出可取证的专家判断与评审清单，
不内嵌其他技能正文；能力经 `dependence/` 声明，遇不明强制派 `file_ops` 联网取证。

## 执行路径

- **顾问**：初始化 → 问题解析 → 领域定位 → 知识检索 → 取证探查 → 专家判断 → 评审清单 →
  重构建议 → 输出交付 → 收尾（横切：浏览器学习）
- **修改**：初始化 → 修改流程 → 完成

## 结构

- [`SKILL.md`](SKILL.md)：入口（YAML frontmatter）。
- [`agent/`](agent/)：四格式一句话提示词。
- [`branch/流程/`](branch/流程/流程.md)：流程节点（文件夹名=流程名）。
- [`asset/`](asset/asset.md)：机读知识树 + 九叶细则 + 评审清单 + 模板。
- [`references/`](references/references.md)：知识库（官方文档/著作/书目摘要）。
- [`dependence/`](dependence/dependence.md)：依赖声明 + `deps.json`（每条附 `source_url`）。
- [`resistance/`](resistance/resistance.md)：约束与兜底（git 工作流、五大机制）。
- [`planned_tasks/`](planned_tasks/README.md)：计划任务声明（到期由 SMS 调度器执行）。
- [`scripts/`](scripts/scripts.md)：薄探针脚本（英文名）。
- [`update/update.md`](update/update.md)：自更新接口（本体唯一写盘通道）。
- [`CHANGELOG.md`](CHANGELOG.md) / [`LICENSE`](LICENSE)：版本记录与 MIT 许可。

## 知识树（九叶）

object-model-meta · threading-ownership · widgets-ui · qtquick-qml · models-view ·
rendering-performance · build-deploy · i18n-a11y · testing-migration

## 红线摘要

- 悬空链接为 0（`python -B scripts/check_links.py --root .`）；所有 .md ≤ 50 行。
- 变更先入 `tmp/` 镜像，再经 `update/` compare → release；禁止删除 `resistance/` 约束。
- 未确证条目标 `[本地]`，严禁臆造 URL；缺 `source_url` 即判不合格。
- Git：功能分支 → `dev` → `main`，本地提交；推送前须用户确认。

## 相关

- [流程总览](branch/流程/流程.md) · [知识树索引](references/知识树/知识树.md)
