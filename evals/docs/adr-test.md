# ADR-007: Adopt PostgreSQL for User Data Storage

## Context

The current user data storage uses MySQL 5.7. As user volume grows, we face connection limits and complex query performance issues. The team evaluated whether to migrate user data to a dedicated PostgreSQL cluster or a NoSQL solution.

## Decision

Migrate user data (accounts, profiles, settings) from MySQL to a dedicated PostgreSQL 16 cluster. We chose PostgreSQL over MongoDB.

## Rationale

- PostgreSQL supports ACID transactions, which user accounts require
- The team has more PostgreSQL experience than MongoDB
- Row-based storage fits user profile access patterns

## Alternatives Considered

- MongoDB: rejected due to weaker transaction support

## Consequences

- **Positive**: better connection handling, richer indexing
- **Negative**: migration cost estimated at 3 person-months; existing reporting queries (which join across 12 tables) must be rewritten
- Existing MySQL stays as the source of truth during the 6-month migration window

## Impact Scope

Affects: user-service, billing-service, notification-service. The analytics pipeline is not affected because it reads from the data warehouse, which continues to read MySQL directly during migration.

## Notes

- Migration starts 2026-03-01 and the ADR was written on 2026-01-10, after the migration plan was already approved
- The team will keep a rolling window of MySQL data for audit purposes
