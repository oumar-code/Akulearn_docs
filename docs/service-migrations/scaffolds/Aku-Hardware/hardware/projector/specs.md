# Aku Projector Module — Specification

**Revision:** A (Prototype)

---

## 1. Display Requirements

| Parameter | Minimum | Preferred |
|-----------|---------|-----------|
| Brightness | 2000 ANSI lumens | 3000+ ANSI lumens |
| Native resolution | 1280×800 WXGA | 1920×1080 FHD |
| Contrast ratio | 15 000:1 | 20 000:1 |
| Throw ratio | 1.1–2.0 | Short-throw ≤ 1.0 preferred |
| Projection size | 60–120 inch diagonal | 80–100 inch target |
| Keystone correction | Manual vertical ±40° | Auto keystone |
| Lamp technology | LED (preferred) or DLP | LED only (no mercury) |
| Lamp life | ≥ 20 000 hours | ≥ 30 000 hours |

## 2. Connectivity

| Interface | Required | Notes |
|-----------|----------|-------|
| HDMI 1.4 input | Yes | Video + audio from Edge Hub |
| USB-A 2.0 | Yes | Media player (USB stick fallback) |
| 3.5 mm audio out | Optional | External speaker connection |
| VGA | No | Legacy — not required |

## 3. Power

| Parameter | Value |
|-----------|-------|
| Input | 90–240 V AC, 50/60 Hz auto-switching |
| Typical power | 60–80 W (LED models) |
| Standby power | < 0.5 W |
| Power factor | > 0.9 |
| Source | Edge Hub inverter-charger 230 V AC output |

## 4. Environmental

| Parameter | Value |
|-----------|-------|
| Operating temperature | 0 °C to +45 °C |
| Storage temperature | -20 °C to +60 °C |
| Humidity | 20 %–80 % non-condensing |
| Altitude | ≤ 3000 m (de-rate brightness above 1500 m) |
| IP rating | None (indoor use only) |

## 5. Physical

| Parameter | Value |
|-----------|-------|
| Weight | < 3 kg (portable tier) |
| Noise | < 35 dB (normal mode) |
| Cooling | Internal fan; ensure 10 cm clearance on all sides |
| Mounting | 1/4"-20 UNC tripod socket (bottom) |

## 6. Content Format Support

The Aku-SmartBoard software (KMP/Compose Desktop) outputs content via the RPi
HDMI port. The projector must accept and display:

| Format | Notes |
|--------|-------|
| 1280×720 @ 60 Hz | Standard HD output from RPi |
| 1920×1080 @ 30 Hz | HD output (production RPi HDMI) |
| Colour space | sRGB / BT.709 |
