<!--
COPILOT_PROMPT:
Generate a complete Aku Platform overview. Cover executive summary, three tiers (Aku Edge Hub, Aku Super Hub, Aku IG-Hub),
Meshstatics (Network Provider and Data Center), key services (Aku Learn, Aku DaaS, Aku eSIM),
operational principles and a short diagram description section for a designer.
# Aku Platform Overview
 
## Executive Summary

The Aku Platform is a unified, tiered ecosystem that delivers localized compute, resilient connectivity, and compliant cross-border data services across the ECOWAS region. It combines edge hardware (Aku Edge Hubs), regional processing (Aku Super Hubs), and a logically centralized but physically distributed global control plane (Aku Interstate Gateway Hub — IG-Hub). Meshstatics (Network Provider and Data Center) provides the foundational fabric that hosts and connects these tiers.

## Core Architectural Tiers

### Aku Edge Hub (Tier 1)

Aku Edge Hubs are ruggedized edge compute nodes deployed at schools, clinics, community centers and micro data-centers. They provide local content caching, IoT integration, basic AI inference, and offline-first experiences. Edge Hubs support solar/wind hybrid power and are optimized for low-bandwidth, intermittent connectivity.

### Aku Super Hub (Tier 2)

Aku Super Hubs are national/regional control planes that aggregate telemetry and data from clusters of Edge Hubs, provide regional API gateways, perform heavier analytics and model fine-tuning, and orchestrate updates and configuration for edge fleets.

### Aku Interstate Gateway Hub (IG-Hub - Tier 3)

The IG-Hub is the Tier 3 logical control plane and clearing house for cross-border operations. It handles anonymized metadata exchange, financial clearing (Aku Coin settlement), policy & compliance enforcement, and global model management.

## Foundational Infrastructure

### Meshstatics (Network Provider and Data Center)

"Meshstatics" represents the physical network provider and data center layer that hosts core network functions, regional caches, and interconnection points. Meshstatics supports carrier-grade backhaul, IX/peering points, and co-location for the IG-Hub.

## Key Services of the Aku Platform

- Aku Learn (education delivery and local AI tutoring)
- Aku DaaS (Data-as-a-Service: anonymized insights and secure datasets)
- Aku eSIM (embedded SIM provisioning and mobile connectivity)
- Aku Workspace (AI-Native Productivity Suite — see below)

### Aku Workspace (AI-Native Productivity Suite)

Aku Workspace is the AI-first productivity layer built on top of the Aku Platform. It provides natural-language-driven tools for data analysis, document and presentation generation, communication, and project management. The core interaction layer is the Aku AI Assistant which understands user intent, leverages contextual memory, and orchestrates distributed compute across Edge Hubs, Super Hubs, and the IG-Hub to perform tasks efficiently and securely.

## Overall Vision: The Aku AI-Native Ecosystem

The Aku Platform is evolving beyond infrastructure to deliver an "Intuitive Intelligence" Workspace, redefining productivity through AI-first, natural language interaction. This vision aims to remove technical barriers, making powerful data analysis, document creation, and communication effortless for all users. The Aku AI Assistant, leveraging distributed intelligence from Edge Hubs, Super Hubs, and the IG-Hub, will be the core interaction layer for all Aku Workspace applications.

## Diagram Description (for designers)

Create a multi-tier diagram showing:

- Tier 1 (Edge): many Aku Edge Hubs with local devices and sensors. Show offline cache and solar/wind power.
- Tier 2 (Super): regional Aku Super Hubs aggregating telemetry, performing analytics and model fine-tuning.
- Tier 3 (IG-Hub): a logically centralized control plane for anonymized metadata exchange, financial clearing and global model orchestration.
- Meshstatics underlying all tiers as network provider and data centers.
- Services (Aku Learn, DaaS, eSIM, Aku Workspace) running across tiers with arrows showing data flow and control lines (anonymized data to IG-Hub).

---

For full details on components, see the `docs/components/` and `docs/services/` folders.
