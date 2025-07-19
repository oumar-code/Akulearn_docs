# Akulearn Architectural Decision Records (ADRs)

This page documents key architectural decisions made during the design and development of the Akulearn platform. Each ADR includes its title, status, a summary, and the full content for reference.

---

## ADR 001: Adopt Microservices Architecture

**Status:** Accepted

**Summary:**
Akulearn will use a microservices architecture to enable independent deployment, scalability, and modularity. This approach supports rapid feature delivery, resilience, and future extensibility.

**Full Content:**
Akulearn's platform will be built as a set of loosely coupled microservices, each responsible for a distinct business capability (e.g., authentication, content management, AI/ML, blockchain credentialing). Services will communicate via REST/gRPC for synchronous operations and Kafka for asynchronous event-driven messaging. Containerization (Docker) and orchestration (Kubernetes) will be used for deployment and scaling. This decision enables teams to work independently, improves fault isolation, and allows for technology diversity where needed.

---

## ADR 002: Event-Driven Communication with Kafka

**Status:** Accepted

**Summary:**
Kafka will be used as the central event bus for asynchronous communication between microservices, supporting scalability and decoupling.

**Full Content:**
Akulearn's microservices will publish and consume events via Apache Kafka. This enables non-blocking, high-throughput communication, supports real-time analytics, and decouples service dependencies. Event schemas will be versioned for backward/forward compatibility. Idempotency will be enforced in consumers to handle duplicate messages. This approach is critical for features like learning event tracking, content processing triggers, and projector data sync.

---

## ADR 003: Polyglot Persistence

**Status:** Accepted

**Summary:**
The platform will use multiple database technologies: PostgreSQL for structured transactional data, MongoDB for flexible content metadata, and IPFS/Filecoin for decentralized storage.

**Full Content:**
Akulearn will adopt polyglot persistence to optimize data storage for different use cases. PostgreSQL will be used for user profiles, subscriptions, and transactional records. MongoDB will store content metadata, activity logs, and flexible documents. IPFS/Filecoin will handle large, unstructured content (videos, images) for decentralized access and redundancy. This decision improves performance, scalability, and data integrity across the platform.

---

## ADR 004: API-First Development with OpenAPI

**Status:** Accepted

**Summary:**
All APIs will be designed and documented using OpenAPI/Swagger before implementation, enabling parallel development and consistent interfaces.

**Full Content:**
Akulearn's development teams will adopt an API-first approach. API contracts will be defined in OpenAPI/Swagger, reviewed, and agreed upon before backend and frontend implementation begins. This ensures clear boundaries, enables automated client SDK generation, and supports thorough testing. API versioning will be enforced for backward compatibility. This decision streamlines development and improves integration quality.

---

## ADR 005: Secure Authentication & RBAC

**Status:** Accepted

**Summary:**
Authentication will use JWTs, and Role-Based Access Control (RBAC) will be enforced across all services for security and compliance.

**Full Content:**
Akulearn will implement stateless authentication using JSON Web Tokens (JWTs). All API endpoints will require authentication, and RBAC will be used to restrict access based on user roles (learner, facilitator, admin, etc.). Sensitive data will be encrypted in transit (HTTPS) and at rest. Secrets will be managed via secure vaults (AWS Secrets Manager, HashiCorp Vault). This decision ensures robust security and regulatory compliance.

---

## ADR 006: Containerization & Kubernetes Orchestration

**Status:** Accepted

**Summary:**
All services will be containerized with Docker and orchestrated using Kubernetes for deployment, scaling, and management.

**Full Content:**
Akulearn's microservices will be packaged as Docker containers. Kubernetes will manage service deployment, scaling, health checks, and rolling updates. Infrastructure as Code (Terraform) will be used for provisioning cloud resources. This approach provides portability, resilience, and operational efficiency, supporting rapid iteration and high availability.

---

For more ADRs and updates, see this page as the project evolves.
