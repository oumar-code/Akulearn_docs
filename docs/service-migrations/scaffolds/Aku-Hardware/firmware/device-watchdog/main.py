"""
Aku Edge Hub — Hardware Device Watchdog Firmware
Target: Raspberry Pi Pico (RP2040) running MicroPython
Version: 1.0.0

Supervises the Aku Edge Hub SBC (Raspberry Pi 4B or Jetson Orin Nano).
If the SBC stops sending a "PING" followed by a newline character over UART
within the watchdog timeout window, this firmware cuts power to the SBC via a
relay and restores it after a short reset delay — performing a hard reboot.

Wiring:
  Pico GP0 (UART0 TX) → (optional: send commands to SBC)
  Pico GP1 (UART0 RX) → SBC UART TX (receive "PING\\n" heartbeat)
  Pico GP15            → Relay IN (HIGH = SBC powered ON, LOW = power cut)
  Pico GP16            → Error LED anode via 330 Ω (blinks on repeated resets)
  Pico USB             → Host PC (debug serial / config)
  Pico VBUS (pin 40)   → Relay VCC (5 V)
  Pico GND (pin 38)    → Relay GND

Relay wiring:
  Relay COM → 5 V supply input to SBC (USB-C PD buck converter input)
  Relay NO  → SBC 5 V input (power ON by default)
  Relay NC  → (unconnected)

Operation:
  1. On startup the relay is closed (SBC powered ON), error LED off.
  2. Every second the watchdog checks for a fresh PING on UART.
  3. If no PING is received within WATCHDOG_TIMEOUT_S seconds, the relay is
     opened (SBC power cut) for RESET_HOLDOFF_S seconds, then closed again.
  4. After MAX_RESETS consecutive resets without a successful heartbeat, the
     error LED blinks continuously and the watchdog stops attempting resets
     (manual intervention required).
"""

import time

from machine import UART, Pin  # type: ignore[import]  # MicroPython built-in

# ── Configuration ─────────────────────────────────────────────────────────────
HEARTBEAT_INTERVAL_S: int = 30    # SBC sends "PING\\n" every 30 s
WATCHDOG_TIMEOUT_S: int = 90      # 3 × heartbeat interval
RESET_HOLDOFF_S: int = 5          # Duration SBC power is cut during reset
MAX_RESETS: int = 3               # Max resets before alerting and halting

# ── Pin assignments ────────────────────────────────────────────────────────────
RELAY_PIN: int = 15    # HIGH = SBC powered, LOW = power cut
ERROR_LED_PIN: int = 16

# ── UART (receive heartbeat from SBC) ─────────────────────────────────────────
UART_ID: int = 0
UART_BAUD: int = 115_200


def _blink_error(led: Pin, count: int = 5, interval_ms: int = 200) -> None:
    """Blink the error LED `count` times."""
    for _ in range(count):
        led.on()
        time.sleep_ms(interval_ms)
        led.off()
        time.sleep_ms(interval_ms)


def main() -> None:
    """Main watchdog loop."""
    # Initialise UART for heartbeat reception
    uart = UART(UART_ID, baudrate=UART_BAUD, tx=Pin(0), rx=Pin(1))

    # Relay — default HIGH = SBC powered ON
    relay = Pin(RELAY_PIN, Pin.OUT, value=1)

    # Error LED — default OFF
    error_led = Pin(ERROR_LED_PIN, Pin.OUT, value=0)

    last_ping_ts: float = time.time()
    reset_count: int = 0
    rx_buf: str = ""

    print("Aku Device Watchdog v1.0.0 — monitoring SBC heartbeat")
    print(f"  Timeout     : {WATCHDOG_TIMEOUT_S} s")
    print(f"  Reset hold  : {RESET_HOLDOFF_S} s")
    print(f"  Max resets  : {MAX_RESETS}")

    while True:
        # ── Read available UART bytes ─────────────────────────────────────────
        if uart.any():
            chunk = uart.read(uart.any())
            if chunk:
                rx_buf += chunk.decode("utf-8", "ignore")

        # ── Parse complete lines ──────────────────────────────────────────────
        while "\n" in rx_buf:
            line, rx_buf = rx_buf.split("\n", 1)
            line = line.strip()
            if line == "PING":
                last_ping_ts = time.time()
                reset_count = 0          # successful heartbeat — reset the counter
                error_led.off()

        # ── Check for timeout ─────────────────────────────────────────────────
        elapsed = time.time() - last_ping_ts
        if elapsed >= WATCHDOG_TIMEOUT_S:
            reset_count += 1
            print(
                f"[WATCHDOG] No heartbeat for {elapsed:.0f} s "
                f"— reset #{reset_count}"
            )

            if reset_count > MAX_RESETS:
                # Too many consecutive resets — alert and halt
                print(
                    "[WATCHDOG] ERROR: exceeded max resets "
                    f"({MAX_RESETS}). Manual intervention required."
                )
                while True:
                    _blink_error(error_led, count=10, interval_ms=100)
                    time.sleep(2)

            # Blink error LED to signal reset in progress
            _blink_error(error_led, count=3)

            # Cut SBC power
            relay.off()
            print(f"[WATCHDOG] SBC power cut — holding for {RESET_HOLDOFF_S} s")
            time.sleep(RESET_HOLDOFF_S)

            # Restore SBC power and reset heartbeat timer
            relay.on()
            last_ping_ts = time.time()
            print("[WATCHDOG] SBC power restored — waiting for heartbeat")

        time.sleep(1)


main()
