# brain/decision_maker.py — Decides what Guido does based on intent

import logging
from config import Config
from communication.serial_bridge import SerialBridge
from communication.voice_speaker import VoiceSpeaker
from brain.navigation_map import NavigationMap
from perception.rfid_reader import RFIDReader


log = logging.getLogger(__name__)


class DecisionMaker:
    def _on_room_arrived(self, uid: str):
       room = self.nav_map.locate_by_rfid(uid)
       if room:
           self.speaker.say(f"Nous sommes arrivés à {room['name']}")
           
    def __init__(self, serial: SerialBridge, speaker: VoiceSpeaker):
        self.serial  = serial
        self.speaker = speaker
        self.nav     = NavigationMap()
        self.rfid = RFIDReader(on_scan_callback=self._on_room_arrived)
        self.rfid.start()
        log.info("DecisionMaker initialized")

    def handle(self, intent: str, entities: dict):
        """
        Main entry point — receives intent + entities from NLU
        and decides what to do.
        """
        log.info(f"Handling intent: '{intent}' | entities: {entities}")

        if intent == "GUIDE_TO":
            self._handle_guide_to(entities)

        elif intent == "UNKNOWN":
            self._handle_unknown()

        else:
            # Should never happen since NLU validates intents
            # but just in case
            log.warning(f"Unrecognized intent: '{intent}'")
            self._handle_unknown()


    # ----------------------------
    # Intent Handlers
    # ----------------------------

    def _handle_guide_to(self, entities: dict):
        destination = entities.get("destination", None)

        # No destination extracted
        if not destination:
            log.warning("GUIDE_TO intent but no destination found")
            self.speaker.say("Sorry, I didn't catch where you want to go. Can you repeat?")
            return

        # Check if destination exists in our map
        location = self.nav.find(destination)

        if not location:
            log.warning(f"Destination '{destination}' not found in navigation map")
            self.speaker.say(f"Sorry, I don't know where {destination} is.")
            return

        # All good — confirm and send command to Arduino
        log.info(f"Guiding to: {location['name']} | command: {location['command']}")
        self.speaker.say(f"Sure! Guiding you to {location['name']}.")
        self.serial.send(location["command"])


    def _handle_unknown(self):
        log.info("Unknown intent — rejecting request")
        self.speaker.say("Sorry, I can't help with that.")
