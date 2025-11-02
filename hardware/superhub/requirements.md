# Super Hub - Requirements & COTS Selection

This document captures the Super Hub (Tier 2) functional and hardware requirements, focusing on a rack-mounted, redundant, and secure national node.

## Functional Requirements
- Aggregate data from multiple Edge Hubs, perform regional AI/ML workloads, and provide storage and APIs for downstream services.
- Accommodate batch model training and inference; support GPU acceleration where necessary.

## Compute & Storage
- Rack form factor: 1U or 2U chassis.
- CPUs: Intel Xeon Scalable or AMD EPYC; pick SKU based on local procurement and cost-performance.
- GPUs: NVIDIA H100/A100 for heavy workloads, or multiple NVIDIA A30/A40 for balanced throughput.
- Storage: NVMe SSDs for hot data, with larger SATA/NAS storage for archival. Consider RAID and hot-swap trays.

## Networking
- Backbone connectivity: 10/25/40GbE depending on aggregation requirements.
- Redundant NICs and BMC management for remote operations.

## Power & Cooling
- Dual redundant PSUs; integrated fans and airflow optimized for the chosen chassis.

## Security
- TPM 2.0 or hardware root-of-trust on motherboards.
- Optionally use HSMs for key storage in critical co-located racks.

## Procurement Notes
- Prefer commercial vendors with local or regional distribution to reduce lead times.
