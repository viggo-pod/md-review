# 架构设计描述：订单服务（ADD）

## 概述

本文档描述订单服务的架构，负责订单创建、支付状态同步与库存预占。

## 逻辑视图

系统由以下模块组成：order-api、order-core、payment-client、inventory-client、order-store。
order-api 接收请求并委托给 order-core；order-core 调用 payment-client 与 inventory-client。

## 物理视图

部署由负载均衡后的 3 个 order-api 实例与单个 MySQL 实例组成。（无更多拓扑细节。）

## 数据视图

订单数据存储在 MySQL 的 order 表中。订单状态机：created → paid → shipped → completed。

## 接口定义

- `POST /v1/orders` — 创建订单。参数：sku、quantity、user_id。返回：order_id。
- `POST /v1/orders/{id}/cancel` — 取消订单。

## 数据流

1. 客户端调用 order-api → order-core 校验
2. order-core 调用 payment-client 扣款
3. 支付结果写入 order 表
4. order-core 调用 inventory-client 预占库存

## 约束与假设

- 假设 payment-client 可用性 99.9%
- 假设 inventory-client 幂等

## 质量属性

- 性能：订单创建 P95 < 200ms
- 可用性：99.9%
- 安全：全站 HTTPS
