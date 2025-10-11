# Akulearn Platform Documentation

## Overview
Akulearn is a smart, modular classroom platform for teachers and students, integrating AI, collaboration, analytics, and hardware monitoring.

## Microservices
- **AI Tutor:** Real-time Q&A, hints, explanations
- **Polls/Q&A:** Live polls, quizzes, and feedback
- **Hub Integration:** Sync lessons, quizzes, resources
- **Analytics:** Progress tracking, engagement, reports
- **Classroom Management:** Attendance, device control
- **Accessibility:** TTS, multi-language, UI options
- **Hardware Integration:** Sensors, energy management

- **Marketplace:** Item listing, buying, and Aku Coin transactions
- **Community:** Compensation logic and member data

## Frontend
- Vue dashboard for real-time status, analytics, and collaboration
- Touch-friendly, large-format UI for smart boards/TVs

- Marketplace & Community dashboards for item transactions and compensation tracking

## Deployment
- See `DEPLOYMENT.md` for build, run, and update instructions
- Use CI/CD workflows for automated testing and deployment

- Monitoring dashboards expanded for CPU, memory, SQL, and pod restarts
- Automated alerting for infra incidents (email notifications)

## Troubleshooting
- Check logs for errors in backend and frontend
- Use maintenance checklist for hardware issues

## Training
- See guides for teachers/admins on using dashboard, uploading content, and managing devices

# Aku Network: Community-Owned Decentralized Telecom Infrastructure

## Strategic Vision

Akulearn leverages decentralized edge computing (Aku Hubs/mini data centers) to build a competitive, community-focused telecommunications network. This model creates a Community-Owned, Decentralized Telecommunications Infrastructure, differentiating us from legacy providers (MTN, Airtel) by prioritizing local processing, peer-to-peer data exchange, and community ownership.

## Phased Rollout Strategy

**Phase 1: Technological Foundation (Decentralized Mesh Network)**
- Transition from Hub-and-Spoke to True Mesh Network across regions.
- Upgrade Aku Hubs to Mesh Nodes with long-range radios (Wi-Fi/LoRa).
- Integrate Mobile-Edge-Computing (MEC) for local voice/video/data routing and caching.
- Develop Aku Embedded SIM (eSIM) OS layer for device auto-connect and bandwidth sharing.
- Utilize solar-equipped public infrastructure for continuous coverage.

**Phase 2: Community & Economic Model**
- Launch "Aku Node Partner" program: Incentivize hosting/powering Hubs with Aku Coin, free/subsidized access, and micro-payments.
- Prioritize local/state traffic for ultra-low latency and cost efficiency.
- Implement Aku Coin for partner compensation and transparent, decentralized ownership.

**Phase 3: State Rollout Strategy**
- Pilot in a single LGA, then expand in rings to maximize coverage and efficiency.
- Establish state backbone with minimal global backhaul.
- Deploy in high-traffic zones, leveraging existing solar infrastructure.

## Technical Architecture

- See `meshstatic_config.yaml` for MeshStatic dual-role (Data Center/Network Provider) configuration across all tiers.
- Refer to `diagrams/mesh_network.md` and architectural blueprints for visualizations.
- Hardware: Edge Hubs (Jetson Nano/Orin), Super Hubs, Interstate Gateway Hubs, solar power, multi-radio interfaces.
- Software: Aku OS (Linux, containerized microservices), Mesh Agent, PowerDaemon, Telemetry Agent, Edge Caching, Local API Gateway.

## Architecture Diagrams

- **MeshStatic Multi-Tier Architecture:** See `diagrams/mesh_network.md` and `meshstatic_config.yaml` for the full multi-tier, dual-role node design, failover, and metrics.
- **Aku Network Rollout & Competitive Comparison:** See `diagrams/edge_hub.md` and new diagrams in `diagrams/` for phased rollout, hub/cluster/backbone, and MNO vs. Aku comparison.
- **Aku Cloud PC (DaaS) Architecture:** See `diagrams/aku_daas.md` for multi-network, failover, QoS, and edge compute integration.

## Technical Code Samples: MeshStatic & DaaS Implementation

### Tier 1 (Edge Node)
```go
// Edge Node: Caching, Routing, Fast Reroute, Metrics
package main
import (
    "net/http"
    "time"
)
func cacheHandler(w http.ResponseWriter, r *http.Request) {
    // LRU cache logic (transient/session data)
}
func routeHandler(w http.ResponseWriter, r *http.Request) {
    // Ultra-low-latency routing logic
}
func failoverHandler() {
    // Fast reroute to next available edge node
}
func metricsHandler(w http.ResponseWriter, r *http.Request) {
    // Report DC/NP traffic ratio
    w.Write([]byte("dc_np_ratio: 0.1/0.9"))
}
func main() {
    http.HandleFunc("/cache", cacheHandler)
    http.HandleFunc("/route", routeHandler)
    http.HandleFunc("/metrics/edge", metricsHandler)
    http.ListenAndServe(":8081", nil)
}
```

### Tier 2 (Super Hub)
```python
# Super Hub: Service Discovery, Load Balancing, Local Persistence, Hybrid Failover, Metrics
from fastapi import FastAPI
import redis
app = FastAPI()
r = redis.Redis(host='localhost', port=6379)
@app.get("/discover")
def discover():
    # Cross-tier service discovery logic
    return {"nodes": ["node1", "node2"]}
@app.get("/balance")
def balance():
    # Load balancing logic (round robin)
    return {"strategy": "round_robin"}
@app.get("/persist")
def persist():
    # Local data persistence
    r.set('key', 'value')
    return {"status": "persisted"}
@app.get("/failover")
def failover():
    # Hybrid failover: reroute for NP, replication check for DC
    return {"failover": "hybrid"}
@app.get("/metrics/core")
def metrics():
    # Report DC/NP traffic ratio
    return {"dc_np_ratio": "0.5/0.5"}
```

### Tier 3 (IG-Hub/Backbone)
```python
# IG-Hub: Data Replication, Archival, Minimal Routing, Replication Check Failover, Metrics
from fastapi import FastAPI
app = FastAPI()
@app.post("/replicate")
def replicate():
    # Async data replication logic
    return {"status": "replicated"}
@app.post("/archive")
def archive():
    # Data archival logic
    return {"status": "archived"}
@app.get("/failover")
def failover():
    # Data replication check failover
    return {"failover": "replication_check"}
@app.get("/metrics/persistence")
def metrics():
    # Report DC/NP traffic ratio
    return {"dc_np_ratio": "0.9/0.1"}
```

### Aku Cloud PC (DaaS) Multi-Network Implementation
```python
# DaaS: Micro-VM Orchestration, Streaming Protocol Stub, Multi-Network VPN, AI Input Prediction
from fastapi import FastAPI
app = FastAPI()
@app.post("/start_vm")
def start_vm():
    # Firecracker/Kata micro-VM orchestration
    return {"status": "vm_started"}
@app.post("/stream")
def stream():
    # Streaming protocol (QUIC/WebRTC stub)
    return {"protocol": "ASP"}
@app.post("/vpn")
def vpn():
    # Zero Trust VPN tunnel setup (WireGuard/IPsec)
    return {"status": "vpn_established"}
@app.post("/predict_input")
def predict_input():
    # AI-driven input prediction stub
    return {"prediction": "next_action"}
@app.get("/qos")
def qos():
    # Proactive QoS steering
    return {"network_quality": "excellent"}
```

---
All code samples and configurations are designed to maximize resilience, scalability, and customer satisfaction, supporting multi-network access and proactive QoS. See referenced diagrams for visual architecture.

## Competitive Advantages
- **Efficiency:** Local traffic stays local, minimizing central server and backhaul reliance.
- **Scalability:** Plug-and-play deployment of new Hubs/Nodes.
- **Community Ownership:** Incentivized participation and local employment.
- **Resilience:** Self-healing mesh, solar power, and local caching.

## Key Considerations
- Regulatory compliance (NCC licensing, spectrum usage).
- Security and reliability across distributed, privately-run Hubs.
- Community compensation and training.

---
For more details, see individual microservice docs and integration guides. For technical details on the telecom infrastructure, see `meshstatic_config.yaml`, `ARCHITECTURE.md`, and the diagrams folder.
