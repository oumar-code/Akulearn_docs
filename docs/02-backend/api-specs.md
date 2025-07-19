# Akulearn API Specifications

## Purpose

API specifications define the contract between Akulearn's backend services and client applications (mobile, web, projector OS). They ensure consistency, enable parallel development, and support automated testing and documentation. Akulearn uses the OpenAPI (Swagger) standard for all RESTful APIs.

Below are example OpenAPI specifications for the User Authentication and Content APIs.

---

## User Authentication API (OpenAPI Example)

```yaml
openapi: 3.0.3
info:
  title: Akulearn User Authentication API
  version: 1.0.0
  description: API for user registration, login, and JWT authentication.
servers:
  - url: https://api.akulearn.com/v1
paths:
  /auth/register:
    post:
      summary: Register a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
                role:
                  type: string
      responses:
        '201':
          description: User registered successfully
        '400':
          description: Invalid input
  /auth/login:
    post:
      summary: Login and receive JWT
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                email:
                  type: string
                password:
                  type: string
      responses:
        '200':
          description: Login successful, JWT returned
        '401':
          description: Invalid credentials
```

---

## Content API (OpenAPI Example)

```yaml
openapi: 3.0.3
info:
  title: Akulearn Content API
  version: 1.0.0
  description: API for uploading, retrieving, and managing educational content.
servers:
  - url: https://api.akulearn.com/v1
paths:
  /content/upload:
    post:
      summary: Upload new educational content
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
                title:
                  type: string
                subject:
                  type: string
                grade:
                  type: string
      responses:
        '201':
          description: Content uploaded successfully
        '400':
          description: Invalid input
  /content/{id}:
    get:
      summary: Retrieve content by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Content retrieved
        '404':
          description: Content not found
```

---

For the full API specifications and additional endpoints, see the OpenAPI documentation in this repository.
