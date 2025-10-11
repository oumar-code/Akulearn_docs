# Akulearn Technology Stack

## Aku Coin Model Diagram

```mermaid
graph TD
    Partner[Node Partner] -- Earns Aku Coin --> Wallet[Wallet]
    Wallet -- Spend Aku Coin --> Marketplace[Marketplace]
    Wallet -- Transfer Aku Coin --> OtherUser[Other User]
    Marketplace -- Item Purchase --> Partner
    Community[Community Ownership] -- Compensation --> Partner
```

## Blockchain Integration

All blockchain calls MUST use PolygonService for verified credentials and AkuCoin, as referenced in guardrails.

## Core Technologies

- Python (FastAPI, SQLAlchemy)
- React Native (Mobile)
- PostgreSQL
- Docker, Kubernetes
- AI/ML: NLP, GenAI

## Placeholder for further tech stack details
