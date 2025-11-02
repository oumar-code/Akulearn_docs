# IG-Hub - Co-location & Cloud Requirements

This document outlines the IG-Hub (Tier 3) design considerations: cloud-native gateway architecture, co-location requirements for IXPs, and security controls.

## Cloud Requirements
- Prefer managed services in GCP for staging and scale: GKE, Cloud SQL, Pub/Sub, Vertex AI for model serving.
- Define VM shapes for control plane and data plane; plan for autoscaling and high-availability zones.

## Co-location Requirements
- Minimal physical footprint at IXPs: 1–2U rack space for critical appliances (routers, peering servers, firewall/VPN appliances).
- High-performance routers/switches, fiber transceivers, and direct peering fabric.

## Security & Key Management
- Use HSMs for high-security key management if storing critical identity or credential material in co-located hardware.

## Networking
- Design for multihoming, BGP peering, and low-latency transit to Super Hubs and national backbones.
