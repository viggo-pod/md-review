<div align="center">

# 📝 md-review

场景感知的 Markdown 文档审查技能，加权评分。

[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.1-blue.svg)](https://github.com/viggo-pod/md-review)
[![Skills](https://skills.sh/b/viggo-pod/md-review)](https://skills.sh/viggo-pod/md-review/md-review)
[![ModelScope](https://img.shields.io/badge/ModelScope-viggopod%2Fmd--review-6600ff.svg)](https://www.modelscope.cn/skills/viggopod/md-review)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/viggo-pod/md-review/pulls)

**[简体中文](README-zh.md) · [English](README.md)**

</div>

**优先找出会导致下游实现出错的 bug 与逻辑错误，其次检查文档的场景化必需内容是否完整** —— 风格与排版只是次要关注点。

单次调用审查一份 Markdown 文档，覆盖 21 种文档场景（PRD、API 规范、GDD、TDD、ADR、生命周期设计文档等），或使用通用模式。

## 核心特性

- **Bug 优先定位** —— 逻辑（30%）是最高权重维度：公式/数字矛盾、缺失边界情况、断裂流程。无论聚焦哪些维度，P0（阻断级）问题都会被报告。
- **21 种场景** —— 每种场景带各自的必需内容检查清单（验收标准、5W1H、接口契约、错误码、生命周期交接契约等）。
- **6 个加权维度** —— 逻辑 30%、场景完整性 25%、章节 15%、引用 10%、冗余 10%、格式 10%。**总分 = Σ(维度分 × 权重)**，百分制；每个维度分 = 该维度计分清单/规则索引中满足项的比例 × 100（按适用项计数）。
- **CI 就绪** —— `--solo` 模式带退出码门禁（`--pass-threshold`，默认 75），每份报告末行输出机器可读的 `MD-REVIEW-SUMMARY` 块。
- **自带验证** —— 内置 12 条计数制 evals、测试夹具与模板、触发问句集与一条命令回归（`bash evals/run_self_test.sh`）。

## 场景

场景参数可选；不指定时按通用模式审查（跳过场景完整性维度）。

| 场景 | 文档 | 必需内容关注点 |
|---|---|---|
| `prd` | 产品需求文档 | 需求清单、用户故事、验收标准、5W1H |
| `adr` | 架构决策记录 | 背景 / 决策 / 理由 / 备选方案 / 影响 |
| `add` | 架构设计描述 | 架构视图、质量属性、接口、数据流 |
| `api` | 接口文档 | 接口契约、错误码、鉴权、可运行示例 |
| `brd` | 商业需求文档 | 商业目标、ROI、成本/收益模型、5W1H |
| `mrd` | 市场需求文档 | 市场分析、用户画像、价值主张、5W1H |
| `fsd` | 功能规格说明 | 功能行为、用例、测试用例、验收标准 |
| `gdd` | 游戏设计文档 | 核心循环、数值、测试用例、任务清单 |
| `gdo` | 游戏概述文档 | 执行摘要、核心概念、设计支柱、USP |
| `tdd` | 技术设计文档 | 系统架构、技术栈、编码规范、性能目标 |
| `ldd` | 关卡设计文档 | 关卡布局、玩家路径、挑战配置、节奏 |
| `concept` | 概念设计文档 | 概念吸引力、市场潜力、核心卖点 |
| `intent` | 产品意图文档 | 问题、用户、证据、假设、MVP、非目标 |
| `capability` | 能力分析文档 | 能力契约、依赖、边界、缺口路由 |
| `feature` | Feature Analysis 文档 | 版本化功能清单、验收、蓝本、来源、交接 |
| `research` | 领域借鉴/研究分析 | 来源证据、借鉴映射、许可证边界、交接 |
| `tld` | 任务清单文档 | 任务拆解粒度、依赖、工作量估算、负责人 |
| `tcd` | 测试用例文档 | 正向/边界/异常覆盖、前置条件、可验证预期结果、需求追溯 |
| `decq` | 待决策登记册（决策队列） | 条目编号、open/closed 状态、预填选项、决策结果字段、机器可判定关闭条件 |
| `issue` | GitHub Issue 草稿 | 工单骨架、四种子形态、状态/标签追溯、关闭条件、Fixes #N |
| `gpr` | GitHub PR 描述 | 摘要、变更清单、测试计划、破坏性变更、关联 issue |

## 环境要求

- Python 3（辅助脚本：`scripts/probe.py`、`scripts/analyze_structure.py`、`scripts/extract_refs.py`、`scripts/score.py`、`scripts/validate_path.py`）
- 支持斜杠命令与技能目录的 Claude Code / Claude 兼容 Agent 运行时

## 安装

将 `skills/md-review` 文件夹复制到你的技能目录：

```bash
# Claude Code（用户全局）
cp -r skills/md-review ~/.claude/skills/

# 或项目本地
cp -r skills/md-review <your-project>/.claude/skills/
```

技能由 `SKILL.md` 定义；运行时读取 `references/`（规则 + 各场景检查清单）、使用 `scripts/`（结构分析）与 `example/`（报告模板）。`evals/` 是开发/回归套件，运行时可选。

## 使用

```
/md-review <path> [scenario] [--dimensions 1,2,3,4,5,6] [--format full|summary|fix] [--solo] [--pass-threshold N] [--output file] [json]
```

| 参数 | 作用 |
|---|---|
| `<path>` | 要审查的 Markdown 文件（单文档；先经路径门校验） |
| `<scenario>` | 上面 21 种场景之一；省略则按通用模式 |
| `--dimensions` | 限定特定维度，如 `--dimensions 1,2`（仅逻辑 + 完整性）。P0 判定不受此参数影响 |
| `--format full` | 完整报告（默认） |
| `--format summary` | 仅评分表 |
| `--format fix` | 报告 + 自动修复。仅静默应用安全机械修复（链接文案、填充词替换、回显标题移除、末尾空行）；需判断的项报告为未修复 |
| `--solo` | 非交互模式，供 CI 使用 |
| `--pass-threshold N` | solo 模式总分退出码门禁（默认 75） |
| `--output <file>` | 同时将报告写入文件 |
| `json` | 附加输出机器可读 JSON |

### 模式

- **交互模式（默认）** —— 先展示审查计划并请求批准，再进行完整审查；文件仅在用户批准后才会改动。
- **Solo 模式（`--solo`）** —— 非交互，直接跑完，完整报告写 stdout（指定 `--output` 时同时写文件），始终以 `MD-REVIEW-SUMMARY` 块结尾。

### 退出码（CI 门禁）

- `0` —— 审查完成，无 P0（阻断级）问题，总分 ≥ `--pass-threshold`
- `1` —— 审查完成，但存在 P0 问题或总分低于阈值
- `2` —— 错误（文件缺失、参数非法、无法解码的输入）

### 输出契约

每份报告以机器可读的汇总块结尾：

```
MD-REVIEW-SUMMARY
File: <doc> | P0 bugs: N | Scenario gaps: N | Fixable: N | Generated: {timestamp}
```

使用 `--output` 时，该块也是写入文件的最后一行，CI 可解析 stdout 交接或文件产物。

## 示例

```
/md-review docs/requirements.md prd --solo --pass-threshold 75
```

solo 模式审查一份 PRD；无阻断问题且总分 ≥ 75 时退出 0。

```
/md-review docs/api-spec.md api --format summary
```

仅输出 API 文档的评分表。

## 质量证据

仓库自带评测套件（`evals/`）：

- `bash evals/run_self_test.sh` —— 回归框架：脚本化检查（`verify_scripts.py` 功能点验证、注册表完整性）始终运行；忽略目录 `evals/reports/` 中的本地报告存在时，再执行相应报告检查。
- `evals/docs/` —— 23 份夹具：16 份注入缺陷的场景文档、3 份干净文档，外加二进制/非 UTF-8/编号断裂/通用边界用例。
- `evals/evals.json` —— 12 条计数制评测定义（4 个缺陷场景审查、generic 审查、3 个干净文档精度、错误路径、步骤编号、模糊规则、敏感信息、路径门禁）。
- `evals/reports/` —— 仅保存本地 eval 输出，不纳入 Git，也不公开发布。
- `evals/trigger-eval-set.json` —— 20 条触发/不触发问句，验证技能激活。

## 仓库结构

```
md-review/
├── skills/
│   └── md-review/              # 技能本体
│       ├── references/         # 审查规则
│       │   └── scenarios/      # 各场景检查清单
│       ├── scripts/            # Python 辅助脚本
│       └── example/            # 报告模板
├── evals/                      # 开发/回归套件
│   ├── docs/                   # 测试夹具
│   └── scripts/                # 验证工具
├── README.md
├── LICENSE
└── .gitignore
```

## 许可证

MIT —— 见 [LICENSE](LICENSE)。
