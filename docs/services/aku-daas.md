<!--
COPILOT_PROMPT:
Generate Aku DaaS doc: micro-VMs, streaming protocol (ASP), QoS steering, multi-network VPN, edge placement strategy.
-->
# Aku DaaS (Data-as-a-Service)

<!-- Copilot: expand here -->

## Overview

Aku DaaS is the platform layer responsible for ingesting, processing, anonymizing, storing, and serving aggregated datasets to authorized consumers. It provides APIs used by internal services (including Aku Workspace) and external partners under strict data governance.

## Integration with Aku Workspace

- Aku Workspace will query Aku DaaS for anonymized datasets to power natural-language data insights and visualizations. All queries from Workspace to DaaS must pass through the Data Governance microservice and respect privacy labels and consent.

