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

## Sample: Publishing anonymized metadata via IG-Hub

In some workflows, Super Hubs publish aggregated/anonymized metadata to the IG-Hub which can then be harvested into the DaaS pipeline. Example (curl):

```bash
# Register a Super Hub (admin-only) -> returns an apiKey
curl -X POST \
	-H "X-API-KEY: admin-secret-example" \
	-H "Content-Type: application/json" \
	-d '{"superHubId":"sh-001","countryCode":"NG","publicKey":"pubkey"}' \
	http://localhost:8080/superhubs/register

# Publish anonymized metadata with issued apiKey
curl -X POST \
	-H "X-API-KEY: <issued-apiKey>" \
	-H "Content-Type: application/json" \
	-d '{"superHubId":"sh-001","datasetId":"d-1","anonymizedPayload":{"count":10}}' \
	http://localhost:8080/metadata/publish
```

See `infra/examples/ig_hub_control_panel/README.md` and `infra/examples/super_hub_simulator/` for runnable examples and a demo simulator.

