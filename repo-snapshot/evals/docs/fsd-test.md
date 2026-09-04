# Functional Specification: Promo Code Engine

## Feature Overview

The promo code engine manages campaign codes, validates them at checkout, and applies discounts.

## Functional List

- F-1: Create promo code
- F-2: Validate promo code at checkout
- F-3: Apply discount
- F-4: Revoke promo code

## Feature Behavior

- F-1: Admin creates a code with a discount type and value. The code is active immediately.
- F-2: When a user enters a code at checkout, the system validates it and returns the discount.
- F-3: Discount types are PERCENT and FIXED. A PERCENT code of 20 means 20% off. A FIXED code of 20 means $20 off.
- F-4: Revoked codes are no longer valid.

## Inter-feature Relationships

- F-2 depends on F-1 (codes must exist before validation)
- F-3 is invoked by F-2

## Inputs and Outputs

- F-2 input: code string, order amount. Output: discount amount.
- F-1 input: discount type, value, expiry date. Output: code.

## Processing Logic

Validation logic: check code exists → check not revoked → check not expired → check usage limit.

Usage limit: each code has a max uses field; a code with max uses 100 that has been used 100 times is rejected. A code with max uses 0 means unlimited.

Discount application: for PERCENT codes, discount = order amount × value / 100. For FIXED codes, discount = min(value, order amount).

## Exception Handling

(Not described.)

## Boundary Conditions

(Not described.)

## Usage Scenarios

- A user applies a promo at checkout
- An admin creates a seasonal campaign

## Test Cases

(Not described.)
