# main.py — Entry point of Guido, boots everything up

import time
import logging
from config import Config
from perception.voice_listener import VoiceListener
from perception.camera import Camera
from brain.nlu import NLU
from brain.decision_maker import DecisionMaker
from communication.serial_bridge import SerialBridge
from communication.voice_speaker import VoiceSpeaker

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s"
)
log = logging.getLogger(__name__)


def boot():
    log.info("Booting Guido...")

    # Initialize all components
    config        = Config()
    serial        = SerialBridge(port=config.SERIAL_PORT, baudrate=config.BAUDRATE)
    speaker       = VoiceSpeaker(language=config.LANGUAGE)
    listener      = VoiceListener(language=config.LANGUAGE)
    camera        = Camera(device_index=config.CAMERA_INDEX)
    nlu           = NLU(model_path=config.MODEL_PATH)
    decision      = DecisionMaker(serial=serial, speaker=speaker)

    log.info("Guido is ready!")
    speaker.say("Hello, I am Guido. How can I help you?")

    return listener, camera, nlu, decision


def main():
    listener, camera, nlu, decision = boot()

    while True:
        try:
            # Step 1 — Listen for user input
            log.info("Listening...")
            user_input = listener.listen()

            if not user_input:
                continue  # Nothing heard, keep listening

            log.info(f"User said: '{user_input}'")

            # Step 2 — Understand the input
            intent, entities = nlu.process(user_input)
            log.info(f"Intent: {intent} | Entities: {entities}")

            # Step 3 — Make a decision and act
            decision.handle(intent=intent, entities=entities)

            # Small delay to avoid hammering the loop
            time.sleep(0.5)

        except KeyboardInterrupt:
            log.info("Shutting down Guido... Bye!")
            break

        except Exception as e:
            log.error(f"Unexpected error: {e}")
            time.sleep(1)  # Chill a bit before retrying


if __name__ == "__main__":
    main()