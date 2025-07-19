# Akulearn Backend Development Team Handbook

## Onboarding

Welcome to the Akulearn backend team! Our mission is to build scalable, secure, and reliable services that power the Akulearn learning ecosystem. New team members should:

- Review the Akulearn project vision, architecture overview, and ADRs
- Set up local development environment (see README and onboarding docs)
- Familiarize yourself with our codebase, microservices, and API contracts
- Join team communication channels and introduce yourself

## Architecture Principles

- **Microservices:** Each service is independently deployable, with clear boundaries and responsibilities
- **API-First:** All APIs are designed and documented before implementation (OpenAPI/Swagger)
- **Event-Driven:** Kafka is used for asynchronous communication and decoupling
- **Polyglot Persistence:** PostgreSQL for transactional data, MongoDB for flexible content, IPFS/Filecoin for large files
- **Security:** JWT authentication, RBAC, encrypted communication, and secrets management
- **Containerization:** Docker and Kubernetes for deployment, scaling, and management

## Development Workflow

- **Agile Sprints:** Work is organized in 2-week sprints with daily standups, sprint planning, reviews, and retrospectives
- **Branching Strategy:** Use GitHub Flow for feature branches, pull requests, and code reviews
- **CI/CD:** Automated pipelines for linting, testing, building, and deploying services
- **Testing:** Unit, integration, and end-to-end tests are required for all public functions and APIs
- **Code Reviews:** All changes must be peer-reviewed before merging
- **Documentation:** Update API specs, ADRs, and runbooks as features evolve

## Tools & Technologies

- **Languages:** Python, Go, Node.js (service-dependent)
- **Frameworks:** FastAPI, Flask, Express, SQLAlchemy, GORM
- **Databases:** PostgreSQL, MongoDB, Redis
- **Messaging:** Kafka
- **DevOps:** Docker, Kubernetes, Terraform, GitHub Actions
- **Monitoring:** Prometheus, Grafana, ELK Stack
- **Security:** JWT, HTTPS, AWS Secrets Manager, HashiCorp Vault
- **Documentation:** OpenAPI/Swagger, MkDocs

## Communication & Collaboration

- **Channels:** Slack/Teams for daily communication, GitHub for code, Confluence for documentation
- **Meetings:** Daily standups, sprint ceremonies, design reviews, and cross-team syncs
- **Knowledge Sharing:** Pair programming, tech talks, and regular code reviews
- **Issue Tracking:** Jira for tasks, bugs, and sprint planning

## Best Practices

- Prioritize readability, consistency, and simplicity in code
- Handle errors explicitly and log context for debugging
- Validate and sanitize all user input
- Write meaningful tests and maintain high coverage
- Keep documentation up-to-date
- Collaborate openly and support your teammates

---

For more details, see the ADRs, architecture docs, and API specifications in this section.
