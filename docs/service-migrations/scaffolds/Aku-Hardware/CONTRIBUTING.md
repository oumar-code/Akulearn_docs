# Contributing to Aku-Hardware

Thank you for helping improve the Aku Platform hardware. This guide covers the
conventions and process for hardware design changes, firmware updates, and
documentation improvements.

---

## Branching Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Stable, reviewed hardware revisions |
| `feat/<description>` | New hardware features or subsystems |
| `fix/<description>` | Bug fixes (wiring errors, BOM corrections, firmware patches) |
| `docs/<description>` | Documentation-only changes |

All changes must be submitted via pull request and reviewed by at least one
hardware team member before merging to `main`.

---

## Commit Message Convention

Follow the [Conventional Commits](https://www.conventionalcommits.org/) standard:

```
<type>(<scope>): <short summary>

[optional body]
[optional footer]
```

**Types:** `feat`, `fix`, `docs`, `test`, `chore`, `refactor`

**Scopes:** `edge-hub`, `projector`, `power-system`, `enclosure`, `firmware`,
`energy-monitor`, `device-watchdog`, `testing`, `ci`

**Examples:**

```
feat(power-system): add 48V battery bus design option
fix(edge-hub): correct NVMe SSD connector pinout in wiring.md
docs(firmware): add mpremote flash instructions to README
test(power-system): add 72-hour burn-in test checklist
```

---

## Hardware Design Changes

When submitting changes to hardware specs, BOMs, or wiring diagrams:

1. **Update the BOM** (`bom.md`) with revised part numbers, quantities, and
   current pricing.
2. **Bump the revision** in the relevant `specs.md` (e.g., `Rev B`).
3. **Update the wiring or assembly guide** if the physical connections changed.
4. **Run hardware testing** per `testing/` procedures before opening a PR.
5. Attach photos or oscilloscope captures to the PR description where relevant.

---

## Firmware Changes

1. All firmware lives in `firmware/`. Each sub-directory is a self-contained
   module for a specific microcontroller or embedded system.
2. Write unit tests where possible (see `firmware/energy-monitor/` for the
   pattern).
3. The `firmware-ci.yml` workflow runs `pylint` and `pytest` on every PR
   targeting `main`. Ensure CI passes before requesting review.
4. Document pin assignments and I²C/SPI addresses in the module `README.md`.

---

## BOM Conventions

Bills of Materials use the following column structure:

| # | Ref | Description | MPN | Qty | Unit Cost (USD) | Supplier |
|---|-----|-------------|-----|-----|-----------------|---------|

- **Ref** — internal reference designator (e.g., `U1`, `C3`, `J2`).
- **MPN** — manufacturer part number.
- Omit pricing for production BOMs where NDA pricing applies; use `TBD`.

---

## Documentation Standards

- Use British English spellings for consistency with the Akulearn style guide.
- All units in SI (watts, volts, amperes, metres, kilograms).
- Markdown tables must be pipe-aligned for readability.
- Diagrams use ASCII art inline in Markdown or Mermaid code blocks.

---

## Code of Conduct

All contributors are expected to treat each other with respect and professionalism.
Harassment, discrimination, or hostile behaviour will not be tolerated.
