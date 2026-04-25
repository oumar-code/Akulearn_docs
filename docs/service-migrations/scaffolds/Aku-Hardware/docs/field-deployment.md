# Field Deployment Guide

This guide covers site selection, installation, commissioning, and handover for
Aku Edge Hub deployments.

---

## 1. Site Survey Checklist

Complete this checklist before confirming a deployment site.

### Solar Resource

- [ ] South-facing roof or open area available (no shading between 9 AM – 3 PM)
- [ ] Estimated minimum daily PSH ≥ 4.5 (use PVGis or NOAA data)
- [ ] Panel mounting structure can bear ≥ 15 kg load

### Wind Resource (if wind turbine installed)

- [ ] Average wind speed at hub height ≥ 3 m/s (use anemometer; record 7-day average)
- [ ] Clear area with 1.5 × rotor diameter exclusion zone around mast base
- [ ] Planning permission / community consent obtained for mast

### Electrical Infrastructure

- [ ] Location for battery enclosure: dry, shaded, ventilated, lockable
- [ ] Cable trench route (solar → charge controller → battery → Edge Hub): ≤ 30 m
- [ ] Earth stake location identified; ground resistance ≤ 10 Ω achievable

### Network Connectivity

- [ ] ISP or satellite modem available at site (for cloud sync)
- [ ] Ethernet cable route from ISP modem to Edge Hub: ≤ 50 m

---

## 2. Installation Sequence

1. **Earth stake** — drive the 1.5 m copper earth stake; measure resistance (≤ 10 Ω).
2. **Mast / panel mount** — erect wind turbine mast or solar panel mounting structure.
3. **Solar panels** — mount panels at correct tilt angle (site latitude ± 5°);
   connect MC4 cables.
4. **Wind turbine** (if applicable) — mount turbine and blades; connect 3-phase AC cable.
5. **Cable trench** — lay PVC conduit; pull solar and turbine cables.
6. **Battery enclosure** — mount battery pack in lockable weatherproof box.
7. **Charge controller** — mount and wire per [`hardware/power-system/`](../hardware/power-system/).
8. **Edge Hub** — mount enclosure (wall or DIN rail); connect 24 V DC from charge controller.
9. **Projector** — mount on ceiling bracket or tripod; connect HDMI and power.
10. **Network** — connect Ethernet from ISP modem to Edge Hub RJ45 uplink port.

---

## 3. Commissioning Tests

After installation:

1. Verify solar panel Voc and polarity at charge controller input terminals.
2. Confirm charge controller bulk / absorption / float LED states.
3. Power on Edge Hub; verify all status LEDs.
4. SSH in and confirm `aku-edgehub` service is `active (running)`.
5. Verify `/metrics` endpoint returns valid power readings.
6. Connect a test device to `Akulearn_Hub_<serial>` Wi-Fi; load content page.
7. Trigger manual cloud sync; confirm data appears in Super Hub dashboard.

---

## 4. Facilitator Handover

Before leaving the site, demonstrate to the facilitator:

1. How to turn the Edge Hub on and off (battery disconnect switch).
2. What the status LEDs indicate (Power, Wi-Fi, Sync).
3. How to connect a device to the Wi-Fi hotspot.
4. How to load content on the projector using the facilitator remote.
5. Who to contact for support (print the Aku support contact card).
6. Monthly maintenance tasks (see [`maintenance.md`](maintenance.md)).

---

## 5. Deployment Record

Complete and submit the deployment record form (digital via Aku-DaaS portal or
paper form) after every site installation:

| Field | Value |
|-------|-------|
| Unit serial | |
| Site name | |
| GPS coordinates | |
| Deployment date | |
| Lead engineer | |
| Facilitator name | |
| Solar PSH (measured) | |
| Wind speed (7-day avg, if applicable) | |
| Initial battery SoC at handover | |
| Any snags / punch-list items | |
