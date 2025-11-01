<!--
COPILOT_PROMPT:
Generate Aku eSIM doc: provisioning flow, SIM policy, network switching, security model for device auth.
-->
# Aku eSIM

<!-- Copilot: expand here -->

## Overview

Aku eSIM provides remote provisioning and lifecycle management for embedded SIMs used by Aku Edge Hubs and connected devices. It integrates with the platform identity system and supports secure OTA provisioning, network selection, and provisioning policies.

## Integration with Aku Platform

- Identity: integrates with the IG-Hub IdP for device identity and attestation.
- Connectivity: interacts with Aku eSIM management APIs to provision profiles and manage network switching.
- Aku Workspace: workspace workflows may surface eSIM provisioning status or require connectivity checks before performing remote tasks; see `docs/services/aku-workspace.md` for cross-linking.

