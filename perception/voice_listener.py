# perception/voice_listener.py — Mic input + Speech-to-Text

import speech_recognition as sr
import logging

log = logging.getLogger(__name__)


class VoiceListener:

    def __init__(
        self,
        language: str       = "en-US",
        energy_threshold: int = 300,     # Mic sensitivity — raise if too noisy, lower if deaf
        pause_threshold: float = 0.8,    # Seconds of silence to consider speech done
        timeout: float      = 5.0,       # Max seconds to wait for speech to START
        phrase_limit: float = 10.0       # Max seconds for a single phrase
    ):
        """
        Sets up the recognizer and microphone.
        Fails gracefully if no mic is found.
        """
        self.language        = language
        self.timeout         = timeout
        self.phrase_limit    = phrase_limit

        self._recognizer = sr.Recognizer()
        self._recognizer.energy_threshold        = energy_threshold
        self._recognizer.pause_threshold         = pause_threshold
        self._recognizer.dynamic_energy_threshold = True   # Auto-adjusts to ambient noise

        self._mic = self._init_mic()

    # ----------------------------
    # Public API
    # ----------------------------

    def listen(self) -> str | None:
        """
        Blocks until the user says something (or timeout expires).
        Returns the recognized text as a string, or None if nothing was heard.
        """
        if self._mic is None:
            log.error("No microphone available — cannot listen.")
            return None

        try:
            with self._mic as source:
                log.info("Adjusting for ambient noise...")
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)

                log.info("Listening for voice input...")
                audio = self._recognizer.listen(
                    source,
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_limit
                )

            return self._transcribe(audio)

        except sr.WaitTimeoutError:
            # Nobody said anything within the timeout — totally normal
            log.debug("Listen timeout — no speech detected.")
            return None

        except Exception as e:
            log.error(f"Unexpected error while listening: {e}")
            return None

    # ----------------------------
    # Internal helpers
    # ----------------------------

    def _transcribe(self, audio: sr.AudioData) -> str | None:
        """
        Sends recorded audio to Google Speech Recognition.
        Returns transcribed text or None on failure.
        """
        try:
            text = self._recognizer.recognize_google(audio, language=self.language)
            log.info(f"Transcribed: '{text}'")
            return text.strip()

        except sr.UnknownValueError:
            # Audio was heard but couldn't be understood
            log.warning("Speech not understood.")
            return None

        except sr.RequestError as e:
            # Network issue or Google API problem
            log.error(f"Google STT request failed: {e}")
            return None

    def _init_mic(self) -> sr.Microphone | None:
        """
        Tries to initialize the default microphone.
        Returns None if no mic is detected, so Guido can still boot.
        """
        try:
            mic = sr.Microphone()
            log.info("Microphone initialized successfully.")
            return mic

        except OSError as e:
            log.error(f"Microphone not found: {e}")
            log.warning("Guido will run without voice input.")
            return None

    @staticmethod
    def list_microphones():
        """
        Utility — lists all detected mic devices with their index.
        Useful when you want to pick a specific mic instead of the default.
        """
        mics = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mics):
            log.info(f"  [{i}] {name}")
        return mics