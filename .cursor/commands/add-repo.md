# 添加开源仓库

将一个新的 LLM Agent + RL 开源项目加入 `README.md` 对应分类表。

## 输入

用户会提供仓库 URL，以及可选的：论文链接、分类建议、日期/组织信息。

## 步骤

1. 打开目标仓库主页与 README，确认它满足收录标准：至少具备 **多轮交互** 或 **工具调用**（含 TIR）。
2. 对照 Taxonomy，选最合适的一类（Base Framework / General / Search & RAG / Web & GUI / Tool / Code & SWE / Reasoning / Multi-Agent / Memory / Embodied / Domain-Specific / Reward & Training / Safety / VLM Agent / Self-Evolution / Environment）。若用户已指定分类，优先按用户指定。
3. 在对应分类表格中新增一行，字段对齐现有格式：
   - Github Repo（带链接）
   - Stars（使用现有 `img.shields.io/github/stars/...` 徽章写法）
   - Date（尽量用 `YYYY.M`）
   - Org
   - Paper Link（无则写 `--`）
4. 若该分类有 `<details>` 技术细节块，为新条目补充简要技术说明（RL 框架、算法、奖励、环境），风格与同表其他条目一致。
5. 同步更新顶部分类徽章数量（对应 category badge 数字 +1），并视情况在 `## Updates` 补一条简短更新说明。
6. 若 `index.html` 仪表盘依赖 README 分类计数，确认改动后数字一致；必要时同步更新。

## 约束

- 不要虚构论文、星标或组织信息；查不到就写 `--`。
- 不要改动无关分类或无关表格样式。
- 保持 Markdown 表格对齐风格与现有条目一致。

## 输出

完成后简要说明：加入了哪个仓库、落在哪个分类、改了哪些文件。
