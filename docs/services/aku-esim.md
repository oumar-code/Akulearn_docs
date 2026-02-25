<!--
COPILOT_PROMPT:
Generate Aku eSIM doc: provisioning flow, SIM policy, network switching, security model for device auth.
-->
# Aku eSIM — Telhone

![Telhone Logo](../images/logos/telhone-logo.svg)

> **Aku eSIM** is the embedded SIM provisioning and MVNO connectivity service of the Aku Platform, branded as **Telhone** in device- and user-facing contexts.

## Overview

Aku eSIM provides remote provisioning and lifecycle management for embedded SIMs used by Aku Edge Hubs and connected devices. It integrates with the platform identity system and supports secure OTA provisioning, network selection, and provisioning policies.

## Brand Identity

The **Telhone** brand (logo: `docs/images/logos/telhone-logo.svg`) is used across:
- Device onboarding screens and SIM activation flows
- MVNO/eSIM provisioning portals and QR code packaging
- Network status and coverage materials
- Partner MNO-facing documentation

## Integration with Aku Platform

- Identity: integrates with the IG-Hub IdP for device identity and attestation.
- Connectivity: interacts with Aku eSIM management APIs to provision profiles and manage network switching.
- Aku Workspace: workspace workflows may surface eSIM provisioning status or require connectivity checks before performing remote tasks; see `docs/services/aku-workspace.md` for cross-linking.

## Containerisation

Aku eSIM (Telhone) is deployed as Docker containers orchestrated by Kubernetes. See [`docs/05-cross-cutting/containerization.md`](../05-cross-cutting/containerization.md) for the full containerisation guide.

Key containers:
| Container | Image | Purpose |
|-----------|-------|---------|
| `telhone-provisioning-api` | `aku/esim-provisioning:latest` | eSIM profile provisioning and lifecycle API |
| `telhone-policy-engine` | `aku/esim-policy:latest` | Network selection and switching policy engine |
| `telhone-ota-agent` | `aku/esim-ota:latest` | Over-the-air profile push agent |

