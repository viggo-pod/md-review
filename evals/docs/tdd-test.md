# 技术设计文档：优惠券引擎（TDD）

## 需求映射

本文档将 FSD 中 F-2「结算时校验优惠码」映射为优惠券校验模块，将 F-1「创建优惠码」映射为优惠券管理模块。

## 总体架构

系统分层：接入层（coupon-api）→ 服务层（coupon-service）→ 存储层（coupon-store）。服务层包含校验引擎与规则引擎两个组件。

## 模块设计

- coupon-api：参数校验与路由，输入 code/order 上下文，输出校验结果
- coupon-service：核心校验逻辑，依赖 rule-engine
- coupon-store：优惠码存储，提供按 code 查询与用量原子自增

## 接口定义

- `validate(code, order)` → `{ valid, discount, reason }`（错误码未定义）
- `create(code, type, value, maxUses)`

## 数据设计

优惠码表字段：code、type、value、max_uses、used_count、revoked、expires_at。数据流向：创建写入 → 校验读取 → 用量更新。

## 技术选型

- 语言：Java 17 + Spring Boot 3
- 存储：MySQL 8 + Redis（用量计数）
- 消息：Kafka（优惠码变更广播）

## 选型理由

Java 生态与现有订单系统一致；Redis 用于高并发用量计数。

## 兼容性

与现有订单系统的技术栈兼容（订单系统同为 Java）。

## 版本锁定

（未锁定任何依赖版本。）

## 编码规范

遵循团队既有 Java 编码规范（Google Java Style）。

## 性能目标

校验接口 P95 < 50ms，压测目标 2000 QPS，但需求映射中 F-2 的峰值流量估算为 5000 QPS。
