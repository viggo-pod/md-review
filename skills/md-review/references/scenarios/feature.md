# Feature Scenario Checklist — Feature Analysis Document

当场景参数为 `feature` 时启用。检查 Feature Analysis 是否形成可被明确消费者使用的权威功能清单。

## Core Questions

1. Feature ID、版本层级和功能边界是否稳定可追踪？
2. 每个 Feature 是否有行为、验收、依赖、蓝本和来源？
3. 跨领域路由和未确认项是否诚实记录？

## Key Focus

版本化 Feature 清单 + 功能详解 + 验收/依赖/来源 + 跨边界关系

## Required Content — count-based scoring

### Product and Inventory

- [ ] **Positioning**：是否说明产品命名、定位、目标用户和非目标？
- [ ] **Unique Feature IDs**：Feature ID 是否唯一且稳定？
- [ ] **Version Applicability**：是否区分不同版本、里程碑或适用范围（或声明适用版本）？
- [ ] **Feature Inventory Table**：是否有包含版本、大类、模块、优先级和来源的总表？

### Per-Feature Detail

- [ ] **Behavior**：每个 Feature 是否说明目标和触发后的行为？
- [ ] **Input and Output**：输入、输出和关键数据对象是否清楚？
- [ ] **Failure and Boundary**：失败、降级和边界条件是否说明？
- [ ] **Acceptance**：每个 Feature 是否至少有一条可观察验收标准？
- [ ] **Dependencies**：依赖、前置条件和实现边界是否声明？
- [ ] **Blueprint**：实现蓝本、复用方式和许可证边界是否说明？
- [ ] **Source**：来源是否能回溯到实际文件、行号或明确外部 URL？

### Boundaries and Handoff

- [ ] **Boundary Dependencies**：跨领域、跨系统或跨模块的消费关系（若有）是否有理由和消费方？
- [ ] **Status and Unknowns**：状态、未知项和待确认项是否有定义且与证据一致？
- [ ] **Handoff Boundary**：是否明确分析与后续设计、实现或交付产物的边界，且没有把分析文档直接写成执行计划？

### 5W1H Check

- [ ] **Who**：谁使用或消费该 Feature？
- [ ] **What**：Feature 提供什么能力？
- [ ] **Why**：解决什么问题或满足什么目标？
- [ ] **When**：在哪个版本或触发时机提供？
- [ ] **Where**：属于哪个领域、系统、模块或接口边界？
- [ ] **How**：如何验收和依赖哪些能力，而不是列实现任务？

## Completeness Issue Markers

- 总表有 Feature，但详解没有验收或来源
- Feature ID 重复、跨版本含义漂移
- 借鉴蓝本没有许可证或改写边界
- 把 Feature Analysis 写成架构、实现计划或执行流程
