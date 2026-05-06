# communication/serial_bridge.py — Sends commands to Arduino via Serial

import serial
import serial.tools.list_ports
import logging
import time

log = logging.getLogger(__name__)


class SerialBridge:

    def __init__(self, port: str = "/dev/ttyUSB0", baudrate: int = 9600, timeout: float = 2.0):
        """
        Opens a serial connection to the Arduino.
        Doesn't crash if the port isn't available — just logs the error
        and marks itself as disconnected.
        """
        self.port     = port
        self.baudrate = baudrate
        self.timeout  = timeout
        self._conn    = None

        self._connect()

    # ----------------------------
    # Public API
    # ----------------------------

    def send(self, command: str):
        """
        Sends a command string to the Arduino.
        Appends a newline so Arduino's Serial.readStringUntil('\\n') works cleanly.
        Retries once if the connection was lost.
        """
        if not self.is_connected():
            log.warning("Serial not connected — attempting reconnect before send...")
            self._connect()

        if not self.is_connected():
            log.error(f"Cannot send '{command}' — serial port unavailable.")
            return

        try:
            payload = f"{command}\n".encode("utf-8")
            self._conn.write(payload)
            self._conn.flush()
            log.info(f"Sent to Arduino: '{command}'")

        except serial.SerialException as e:
            log.error(f"Serial write failed: {e}")
            self._conn = None  # Mark as disconnected for next call

    def is_connected(self) -> bool:
        """Returns True if the serial port is open and alive."""
        return self._conn is not None and self._conn.is_open

    def close(self):
        """Cleanly closes the serial connection."""
        if self.is_connected():
            self._conn.close()
            log.info("Serial connection closed.")
        self._conn = None

    # ----------------------------
    # Internal helpers
    # ----------------------------

    def _connect(self):
        """
        Tries to open the serial port.
        Fails silently (logs error) so the rest of Guido can still boot.
        """
        try:
            self._conn = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            # Arduino resets on serial connect — give it a sec to wake up
            time.sleep(2)
            log.info(f"Serial connected on {self.port} at {self.baudrate} baud.")

        except serial.SerialException as e:
            log.error(f"Failed to open serial port '{self.port}': {e}")
            log.warning("Guido will run without Arduino — serial commands will be dropped.")
            self._conn = None

    @staticmethod
    def list_available_ports() -> list[str]:
        """
        Utility — prints all detected serial ports.
        Useful when you don't know which port your Arduino is on.
        """
        ports = [p.device for p in serial.tools.list_ports.comports()]
        log.info(f"Available serial ports: {ports}")
        return ports