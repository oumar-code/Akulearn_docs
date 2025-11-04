# KPI & Dashboard Specification — Gusau Pilot

## Goals
- Provide real-time visibility into Edge Hub health, usage, Aku Learn engagement, and network metrics. Enable automated alerts for critical failures.

## Key Metrics (to collect)
- Edge Hub health: uptime, CPU temperature, battery voltage, solar input voltage, charge current
- Services: cache hit rate (%), content requests/sec, content sync latency
- Usage: unique students/day, sessions/day, avg session length, teacher logins
- Voice: local call setup success rate, average call duration, minutes by origin/destination
- Network: latency to Super Hub, packet loss, throughput per Edge Hub
- Financial: paid sessions, call revenue (if billing enabled)

## Metric names (Prometheus-friendly examples)
- edge_uptime_percent{site}
- edge_batt_voltage_volts{site}
- edge_solar_voltage_volts{site}
- edge_cpu_temp_celsius{site}
- aku_cache_hit_ratio{site}
- aku_content_requests_total{site}
- aku_unique_students_daily{site}
- voip_call_success_rate{site}

## Dashboards
- Grafana dashboards:
  - Overview: top-line availability, total students, cache hit ratio, alerts
  - Site detail: per-Edge Hub health and recent logs
  - Aku Learn: content popularity & content gaps
  - Network: latency maps and backhaul usage

## Alerts & Thresholds
- Critical: Edge Hub offline > 10 minutes (pager alert)
- Warning: Battery voltage below safe threshold (email alert)
- Performance: cache hit ratio drops below 40% (investigate sync)

## Data retention & privacy
- Telemetry raw logs retained 30 days; aggregated educational telemetry (anonymized) retained 3 years for analytics.
- PII: student identifiers stored locally and only anonymized aggregates sent to Super Hub unless explicit consent exists.

## Implementation notes
- Use lightweight telemetry agent on Edge Hubs to push metrics via HTTPS to a central Prometheus Pushgateway or expose /metrics for scraping via a secure tunnel.
- Central Prometheus + Grafana stack hosted on Super Hub (or cloud during pilot) with alertmanager configured for notifications.
