# 内部分析平台接入说明

## 1. 数据库连接
- 地址: db.internal.corp.example.com:3306
- 连接串: mysql://deploy:P@ssw0rd!2026@db.internal.corp.example.com:3306/payments

## 2. 服务调用
- API Key: sk-live-4f8a2c9b1d7e3f6a0c5b8d1e2f4a6c8b
- Redis 缓存: redis://10.20.30.40:6379

## 3. 示例数据
客服工单示例：用户张伟，身份证号 110101199003074517，联系电话 13800138000。

## 4. 调用规范
- 所有请求需携带 Authorization 头。
- 生产环境使用 HTTPS。

## 5. 结论
本文档供内部团队接入使用。
