# communication/voice_speaker.py — Text-to-Speech, Guido's voice output

import pyttsx3
import logging

log = logging.getLogger(__name__)


class VoiceSpeaker:

    def __init__(
        self,
        language: str  = "en-US",
        rate: int       = 150,       # Words per minute (matches Config.SPEECH_RATE)
        volume: float   = 1.0        # 0.0 → 1.0     (matches Config.SPEECH_VOLUME)
    ):
        """
        Initializes the TTS engine and tries to set a voice
        matching the requested language.
        Falls back to system default if no match is found.
        """
        self.language = language
        self._engine  = None

        self._init_engine(rate, volume)

    # ----------------------------
    # Public API
    # ----------------------------

    def say(self, text: str):
        """
        Speaks the given text out loud, blocking until done.
        Logs a warning instead of crashing if TTS is unavailable.
        """
        if not text or not text.strip():
            log.warning("VoiceSpeaker.say() called with empty text — skipping.")
            return

        log.info(f"Speaking: '{text}'")

        if self._engine is None:
            log.error("TTS engine not available — cannot speak.")
            return

        try:
            self._engine.say(text)
            self._engine.runAndWait()

        except RuntimeError as e:
            # pyttsx3 can throw RuntimeError if called from a bad thread context
            log.error(f"TTS runtime error: {e}")

        except Exception as e:
            log.error(f"TTS unexpected error: {e}")

    # ----------------------------
    # Internal helpers
    # ----------------------------

    def _init_engine(self, rate: int, volume: float):
        """
        Boots up pyttsx3 and configures rate, volume, and voice language.
        """
        try:
            self._engine = pyttsx3.init()
            self._engine.setProperty("rate",   rate)
            self._engine.setProperty("volume", volume)
            self._set_voice(self.language)

            log.info(f"VoiceSpeaker ready — language: {self.language}, rate: {rate}, volume: {volume}")

        except Exception as e:
            log.error(f"Failed to initialize TTS engine: {e}")
            log.warning("Guido will run without voice output.")
            self._engine = None

    def _set_voice(self, language: str):
        """
        Picks the first installed voice whose language tag matches.
        e.g. "en-US" will match voices tagged with "en_US", "en-US", "en", etc.
        Falls back to the system default if nothing matches.
        """
        voices = self._engine.getProperty("voices")

        # Normalize: "en-US" → "en" for broader matching
        lang_prefix = language.split("-")[0].lower()   # "en"
        lang_full   = language.replace("-", "_").lower()  # "en_us"

        for voice in voices:
            voice_id = voice.id.lower()
            langs    = [l.lower() for l in (voice.languages or [])]

            if (
                lang_full   in voice_id or
                lang_prefix in voice_id or
                any(lang_prefix in l for l in langs) or
                any(lang_full   in l for l in langs)
            ):
                self._engine.setProperty("voice", voice.id)
                log.info(f"Voice selected: {voice.name} ({voice.id})")
                return

        # No match — keep system default, just log it
        log.warning(
            f"No voice found for language '{language}'. "
            f"Using system default. "
            f"Available voices: {[v.name for v in voices]}"
        )