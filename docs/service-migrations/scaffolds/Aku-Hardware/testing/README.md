# Testing

Hardware and firmware test procedures for the Aku Edge Hub.

---

## Test Documents

| File | Scope |
|------|-------|
| [`power-system-test.md`](power-system-test.md) | Solar, wind, battery, and inverter acceptance tests |
| [`edge-hub-integration-test.md`](edge-hub-integration-test.md) | Full Edge Hub system integration and burn-in |

---

## Testing Philosophy

1. **Unit test first** — test each subsystem in isolation before assembly.
2. **Acceptance test before deployment** — every unit must pass all checks in
   `edge-hub-integration-test.md` before leaving the workshop.
3. **Document results** — record test readings (voltages, currents, temperatures)
   in the unit's test log sheet; attach to the physical unit's serial number record.
4. **Sign off** — two team members must sign off on each unit before field deployment.

---

## Test Equipment Required

| Item | Specification |
|------|--------------|
| Digital multimeter | DC 0–100 V, 0–20 A; 0.5 % accuracy or better |
| Clamp ammeter | 0–50 A AC/DC, non-contact |
| Oscilloscope | ≥ 50 MHz, 2-channel (I²C signal inspection) |
| DC power supply | 24 V / 5 A variable (simulate charge controller output) |
| Anemometer | 0–20 m/s (field wind speed measurement) |
| Laptop with SSH | For software stack verification |

---

## Related

- [Firmware — Energy Monitor tests](../firmware/energy-monitor/)
- [Assembly Procedure](../hardware/edge-hub/assembly.md)
