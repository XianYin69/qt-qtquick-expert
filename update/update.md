# update（自更新接口）

本技能**本体唯一写盘通道**：内容修改一律「tmp 镜像 → compare → release」，禁止直接编辑。

## 四步

| 步骤 | 动作 | 约束 |
|---|---|---|
| report | 声明本次要改的文件与理由，写入 tmp | 未声明的文件不得出现在镜像里 |
| compare | 逐文件比对 tmp 与本体，出差异清单 | 发现越界路径（其他技能目录）即中止 |
| release | 差异释放到本体 | 已有文件不覆盖许可与约束文件 |
| clean | 删除 tmp 过程工件 | 缓存不得留在 skill 目录 |

## 何时必须走本接口

- 新增/修改 `asset/knowledge/`、`asset/checklists/` 判据；
- 浏览器学习取回的新判据回写；
- `dependence/deps.json` 条目更新（`checked_at`、`source_url_status`）；
- `scripts/` 行为变更；`resistance/` 变更（须同时记 CHANGELOG 与违规后果）。

## 禁止

- 不得借本接口删除 `resistance/` 约束（红线）。
- 不得写入未确证链接；`[本地]` 条目不得伪装 `[联网]`。
- 不得把 `tmp/` 工件纳入 git（`.gitignore` 已含 `tmp/`）。

## 校验

`python -B scripts/check_links.py --root .` · `python -B scripts/knowledge_index.py --check-deps`

## 相关

- [修改流程](../branch/流程/修改流程/修改流程.md) · [垃圾回收机制](../resistance/垃圾回收机制/垃圾回收机制.md)
- [CHANGELOG](../CHANGELOG.md)
