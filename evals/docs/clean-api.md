# Payment Gateway API Reference

> Version: v2.4 | Status: Published | Audience: Integration engineers

## 1. Overview

This document defines the public REST API of the payment gateway. All endpoints require authentication and return JSON. The API enables merchants to create charges, query their status, and issue refunds.

## 2. Conventions

### 2.1 Data Format

Requests and responses use JSON with UTF-8 encoding. Timestamps use RFC 3339 format. Amounts are integers in minor currency units (cents).

### 2.2 Response Envelope

Every endpoint returns the same envelope:

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

`code` is the business error code defined in Section 3. `data` holds the endpoint-specific payload.

### 2.3 Authentication

All requests must include an `Authorization: Bearer <token>` header with a token issued by the merchant portal. Tokens expire after 24 hours; expired tokens return code `401`.

## 3. Error Codes

| Code | Meaning |
|---|---|
| 0 | Success |
| 400 | Invalid parameter (INVALID_PARAM) |
| 401 | Authentication failed (AUTH_FAILED) |
| 402 | Insufficient balance (INSUFFICIENT_BALANCE) |
| 404 | Resource not found (NOT_FOUND) |
| 409 | Duplicate request (DUPLICATE_REQUEST) |
| 429 | Rate limit exceeded (RATE_LIMITED) |
| 500 | Internal server error (INTERNAL_ERROR) |

## 4. Endpoints

### 4.1 Create Charge

`POST /v1/charges`

Creates a charge and returns a payment URL.

Request:

| Parameter | Type | Required | Description |
|---|---|---|---|
| amount | int | yes | Amount in cents, 1..100000000 |
| currency | string | yes | ISO 4217 code, e.g. CNY |
| order_no | string | yes | Merchant order number, unique, 1..64 chars |
| notify_url | string | yes | HTTPS callback URL |

Response (HTTP 200):

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "charge_id": "ch_123456",
    "pay_url": "https://pay.example.com/checkout/ch_123456",
    "expires_at": "2026-08-08T12:00:00Z"
  }
}
```

### 4.2 Retrieve Charge

`GET /v1/charges/{charge_id}`

Returns the current charge state. States: `created` → `pending` → `paid` → `refunded`.

Response (HTTP 200):

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "charge_id": "ch_123456",
    "status": "paid",
    "paid_at": "2026-08-08T10:00:00Z"
  }
}
```

### 4.3 Create Refund

`POST /v1/refunds`

Refunds a paid charge. The refund amount must not exceed the original charge amount.

Request:

| Parameter | Type | Required | Description |
|---|---|---|---|
| charge_id | string | yes | Original charge ID |
| amount | int | yes | Refund amount in cents, 1..original amount |
| reason | string | no | Refund reason, 1..256 chars |

Response (HTTP 200):

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "refund_id": "rf_123456",
    "status": "processing"
  }
}
```

### 4.4 Retrieve Refund

`GET /v1/refunds/{refund_id}`

States: `processing` → `succeeded` | `failed`.

Response (HTTP 200):

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

## 5. Rate Limits and Performance

- Per-merchant rate limit: 100 requests per minute
- Per-merchant hourly cap: 6,000 requests per hour
- When exceeded, the API returns code `429`
- Average response time: 200 ms
- P99 response time: 500 ms

## 6. Notifications

After a charge is paid, the gateway sends an HTTPS POST to the merchant `notify_url`:

```json
{
  "charge_id": "ch_123456",
  "status": "paid",
  "amount": 10000,
  "signature": "hmac-sha256-hex"
}
```

Merchants must acknowledge with HTTP 200. The gateway retries up to 3 times with exponential backoff (1s, 10s, 100s) until acknowledged or 24 hours pass.

## 7. Idempotency

Create-charge and create-refund requests accept an optional `Idempotency-Key` header. Replaying a request with the same key within 24 hours returns the original response and code `409` only when a concurrent duplicate is detected; otherwise the original result is returned.

## 8. Versioning

API versions are path-prefixed (`/v1/`). Breaking changes ship in a new major version; deprecated versions remain available for 12 months after the deprecation notice.

## Appendix

- Signature verification: documented in the merchant portal integration guide (internal)
- Sandbox environment: https://sandbox.pay.example.com
