# 支付网关 API 接口文档

> 版本：v2.3 | 状态：评审中 | 适用对象：接入方开发工程师

## 1. 概述

本文档定义支付网关对外提供的 RESTful API。所有接口均需鉴权后调用。

## 2. 通用约定

### 2.1 数据格式

请求与响应均为 JSON，编码 UTF-8。时间戳格式为 RFC 3339。

### 2.2 通用响应结构

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

`code` 为业务错误码，`data` 为业务数据。

### 2.3 鉴权方式

调用方需在请求头携带签名，签名算法见[鉴权文档](docs/auth.md)。

## 3. 错误码

| 错误码 | 说明 |
|---|---|
| 0 | 成功 |
| 400 | 参数错误 INVALID_PARAM |
| 401 | 鉴权失败 AUTH_FAILED |
| 402 | 余额不足 INSUFFICIENT_BALANCE |
| 404 | 订单不存在 ORDER_NOT_FOUND |
| 409 | 重复请求 DUPLICATE_REQUEST |
| 500 | 系统内部错误 |

## 4. 接口定义

### 4.1 创建支付订单

`POST /v1/charges`

创建一笔支付订单，返回支付链接。签名不合法时返回 400 AUTH_FAILED。

请求参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| amount | int | 是 | 支付金额，单位分 |
| currency | string | 是 | 币种，如 CNY |
| order_no | string | 是 | 商户订单号，唯一 |
| notify_url | string | 是 | 回调地址 |

响应示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "charge_id": "ch_123456",
    "pay_url": "https://pay.example.com/checkout/ch_123456"
  }
}
```

### 4.2 查询订单状态

`GET /v1/charges/{charge_id}`

查询订单状态。

响应示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "charge_id": "ch_123456",
    "status": "paid",
    "paid_at": "2026-08-01T10:00:00Z"
  }
}
```

订单状态流转：created → pending → paid → refunded。

### 4.3 发起退款

`POST /v1/refunds`

对已支付订单发起退款。

请求参数：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| charge_id | string | 是 | 原支付订单 ID |
| amount | int | 是 | 退款金额，单位分，不能超过原订单金额 |
| reason | string | 否 | 退款原因 |

响应示例：

```json
{
  "status": "success",
  "result": {
    "refund_id": "rf_123456",
    "state": "processing"
  }
}
```

### 4.4 查询退款状态

`GET /v1/refunds/{refund_id}`

响应示例：

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "refund_id": "rf_123456",
    "status": "succeeded"
  }
}
```

退款状态流转：processing → succeeded / failed。

## 5. 限流与性能

- 单商户调用频率限制：200 次/分钟
- 单商户每小时调用上限：6,000 次
- 接口平均响应时间：200ms
- 接口 P99 响应时间：0.5ms

## 6. 通知回调

支付成功后，网关会向商户 `notify_url` 异步发送通知，格式为 POST JSON：

```json
{
  "charge_id": "ch_123456",
  "status": "paid",
  "amount": 10000
}
```

## 7. 常见问题

### 7.1 支付成功后未收到回调？

请先检查回调地址是否公网可达，再在商户后台手动同步订单状态。

### 7.2 如何测试？

沙箱环境地址：https://sandbox.pay.example.com，测试卡号见接入文档。

## 附录

- 回调签名验证：[签名验证说明](docs/signature.md)
- SDK 下载：[支付 SDK](https://github.com/example/pay-sdk)
- HTTP 协议示例：见下方

```
POST /v1/charges HTTP/1.1
Host: api.pay.example.com
Authorization: Bearer sk_test_xxx
```
