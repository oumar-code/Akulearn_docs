# .copilot/guardrails.md

## Architecture Constraints

1. All blockchain calls MUST use [@blockchain] PolygonService for Akulearn's verified credentials and AkuCoin.
2. Mobile offline storage MUST implement [@architecture] ADR-004 for secure and resilient local data.
3. Never bypass [@akulearn-core] EncryptionProtocol for any sensitive data transmission or storage.
4. All database interactions MUST be done via SQLAlchemy ORM models, not raw SQL queries (except for migrations).
5. Frontend UI components for the mobile app MUST be developed using React Native.

