# planned_tasks（计划任务声明）

一任务一文件：`pt-<skill>-<slug>.json`。字段名与 SMS 读取端一致，**不得改动**。

## 语义

- 到期由 SMS 调度器读取并执行，执行结果挂 session 关联链；
- **本技能自身不得执行计划任务**（`scripts/` 内无任何调度入口）；
- 删除对应文件即注销该任务。

## 字段

| 字段 | 含义 |
|---|---|
| `id` | 任务唯一标识（同文件名） |
| `skill` | 归属技能 id |
| `title` | 一句话说明 |
| `schedule` | 本地 ISO 时间或 `interval:<秒>` |
| `status` | pending / running / done / paused / failed |
| `action` | 交给调度器的意图 + 参数 |
| `session` | 关联链 session（调度器写） |
| `created_at` | 本地 ISO |

## 模板

见 [`template.json`](template.json)。当前已声明：
[`pt-qt-qtquick-expert-deps-refresh.json`](pt-qt-qtquick-expert-deps-refresh.json)。

## 相关

- [dependence](../dependence/dependence.md) · [收尾](../branch/流程/收尾/收尾.md)
