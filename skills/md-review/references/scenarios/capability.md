# Capability Scenario Checklist — Capability Analysis Document

当场景参数为 `capability` 时启用。检查产品意图/PRD 是否已被转换为可追踪的能力边界和能力契约，但尚未过早变成实现任务。

## Core Questions

1. 每项能力是否有稳定 ID、输入输出和可观察行为？
2. 依赖、失败/降级、边界和验收是否足以交给架构阶段？
3. 缺失项是否区分上游输入缺失与下游消费者缺失？

## Key Focus

能力清单 + 输入输出契约 + 依赖/边界 + 缺口路由

## Required Content — count-based scoring

### Capability Inventory

- [ ] **Goal and Boundary**：是否说明产品目标、能力范围和明确非目标？
- [ ] **Unique Capability IDs**：是否使用唯一、稳定且可引用的能力 ID？
- [ ] **Capability List**：是否列出每项能力、行为、优先级和状态？
- [ ] **Traceability**：每项能力是否能回溯到 PRD/意图或研究来源？

### Capability Contract

- [ ] **Trigger and Behavior**：是否描述触发条件 → 行为 → 结果？
- [ ] **Input and Output**：输入、输出、副作用和关键数据对象是否清楚？
- [ ] **Failure and Degradation**：失败、超时、重试、降级或拒绝路径是否定义？
- [ ] **Boundary and Permissions**：边界值、并发、权限和资源限制是否说明？
- [ ] **Acceptance Assertion**：每项关键能力是否有可观察验收断言？

### Dependencies and Routing

- [ ] **Dependencies**：能力之间及对外部系统的依赖是否声明？
- [ ] **Gap Direction**：缺口是否标记为 `upstream` 或 `downstream`？
- [ ] **LOST Repair**：每个 `LOST` 是否有影响和具体修复动作？
- [ ] **Architecture Handoff**：是否明确交给架构阶段的决策边界？

### 5W1H Check

- [ ] **Who**：谁使用、提供或维护该能力？
- [ ] **What**：能力做什么，产出什么？
- [ ] **Why**：对应哪个产品问题或目标？
- [ ] **When**：何时触发、何时可用？
- [ ] **Where**：在哪个边界、模块或渠道内？
- [ ] **How**：能力如何协作和验收，但不下沉为任务清单？

## Completeness Issue Markers

- 只有能力名称，没有输入输出或行为
- 把模块/技术名当作能力契约
- `LOST` 没有方向和修复动作
- 能力无法追溯到上游需求或证据
