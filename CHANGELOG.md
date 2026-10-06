# CHANGELOG

## 0.1.0 — 2026-10-07

- 初版：Qt 6（Qt 5 遗留注记）与 Qt Quick 薄顾问技能，结构对齐 `cpp-expert` / `python-expert`。
- 知识树九叶：object-model-meta · threading-ownership · widgets-ui · qtquick-qml · models-view ·
  rendering-performance · build-deploy · i18n-a11y · testing-migration（判定不可再拓扑）。
- `asset/knowledge_tree.json` 机读索引 + `asset/knowledge/`（九叶细则）+ `asset/checklists/`。
- `scripts/` 12 个薄探针：classify_topic / knowledge_index / review_checklist / env_probe /
  moc_probe / qml_lint / build_probe / deploy_probe / perf_probe / migration_probe /
  advice_compose / check_links。
- `dependence/deps.json`：Qt 仓库与官方文档条目逐条附 `source_url`（联网核验 2026-10-07）。
- `resistance/`：git 工作流、浏览器学习、薄技能依赖、审查约束、五大机制、沙盒、降级策略。
- `planned_tasks/`：`pt-qt-qtquick-expert-deps-refresh.json`（依赖链接季度复核，由 SMS 调度器执行）。
- MIT `LICENSE`、`.gitignore`（含 `tmp/` 与 IDE 目录）、独立 git 仓（feature → dev → main 本地提交）。
- 违规后果：臆造 URL → 误导迁移决策；跳过取证 → 结论不可复现；直写 main → 无法按步回滚。
