# 同步分类徽章数量

核对并修正 `README.md` 顶部各分类徽章数字，使其与表格实际条目数一致。

## 步骤

1. 统计每个 Taxonomy 分类表格中的仓库行数（只计数据行，不计表头）。
2. 对照顶部 badge 行：
   - Base Framework / General / Search & RAG / Web & GUI
   - Tool / Code & SWE / Reasoning / Multi-Agent
   - Memory / Embodied / Domain-Specific / Reward & Training
   - Safety / VLM Agent / Self-Evolution / Environment
3. 仅当数字不一致时更新对应 badge 中的数字。
4. 若 `index.html` 内有硬编码分类计数，一并核对同步。

## 约束

- 不要改徽章颜色、样式或分类名称。
- 不要增删仓库条目；本命令只修计数。

## 输出

列出每个分类的「原数字 → 新数字」，无变化则说明已一致。
