# brain/rfid_reader.py

import logging
import threading
import time

log = logging.getLogger(__name__)

try:
    import RPi.GPIO as GPIO
    from mfrc522 import SimpleMFRC522
    HARDWARE_AVAILABLE = True
except ImportError:
    HARDWARE_AVAILABLE = False
    log.warning("RFID hardware not available — running in mock mode")


class RFIDReader:
    """
    Wraps the RC522 reader.
    Runs in a background thread, calls a callback when a tag is scanned.
    """

    def __init__(self, on_scan_callback):
        """
        on_scan_callback: function(uid: str) called when a tag is detected
        """
        self.callback = on_scan_callback
        self._running = False
        self._thread = None
        self._last_uid = None
        self._cooldown = 2.0  # seconds — avoids spamming same tag

        if HARDWARE_AVAILABLE:
            self.reader = SimpleMFRC522()

    def start(self):
        self._running = True
        self._thread = threading.Thread(target=self._scan_loop, daemon=True)
        self._thread.start()
        log.info("RFID reader started")

    def stop(self):
        self._running = False
        log.info("RFID reader stopped")

    def _scan_loop(self):
        while self._running:
            uid = self._read_tag()
            if uid and uid != self._last_uid:
                self._last_uid = uid
                log.info(f"RFID tag detected: {uid}")
                self.callback(uid)
                time.sleep(self._cooldown)
            else:
                self._last_uid = None  # reset after cooldown
                time.sleep(0.2)

    def _read_tag(self) -> str | None:
        if not HARDWARE_AVAILABLE:
            return None  # mock mode — inject UIDs manually for testing
        try:
            uid, _ = self.reader.read_no_block()
            if uid:
                return self._format_uid(uid)
        except Exception as e:
            log.error(f"RFID read error: {e}")
        return None

    @staticmethod
    def _format_uid(raw_uid: int) -> str:
        """Converts raw int UID to hex string like 'A3:FF:12:09'"""
        hex_str = f"{raw_uid:08X}"
        return ":".join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))

    def mock_scan(self, uid: str):
        """For testing without hardware — manually inject a UID"""
        log.debug(f"[MOCK] Simulating RFID scan: {uid}")
        self.callback(uid)