# 内部分析平台接入说明

> 以下凭据、地址和个人信息均为 synthetic 测试数据，不对应真实系统或个人。

## 1. 数据库连接
- 地址: db.internal.example.com:3306
- 连接串: mysql://demo_user:EXAMPLE_PASSWORD_2026@db.internal.example.com:3306/payments

## 2. 服务调用
- API Key: sk-live-EXAMPLE000000000000000000000000
- Redis 缓存: redis://10.0.0.10:6379

## 3. 示例数据
客服工单示例：用户示例用户，身份证号 000000000000000000，联系电话 13800000000。

## 4. 调用规范
- 所有请求需携带 Authorization 头。
- 生产环境使用 HTTPS。

## 5. 结论
本文档供内部团队接入使用。
