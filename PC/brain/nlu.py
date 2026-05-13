# brain/nlu.py — Understands user input using Ollama + Gemma 2

from html import entities

import requests
import json
import logging
from PC.brain.prompts import SYSTEM_PROMPT

log = logging.getLogger(__name__)

# The only intents Guido knows about
VALID_INTENTS = ["GUIDE_TO", "UNKNOWN"]


class NLU:
    def __init__(self, model: str = "gemma2:2b", ollama_url: str = "http://localhost:11434"):
        self.model = model
        self.url = f"{ollama_url}/api/chat"
        log.info(f"NLU initialized with model: {self.model}")

    def process(self, user_input: str) -> tuple[str, dict]:
        """
        Takes raw user text, returns (intent, entities) tuple.
        Always returns something — never crashes the main loop.
        """
        log.info(f"Processing input: '{user_input}'")

        try:
            raw_response = self._ask_model(user_input)
            intent, entities = self._parse_response(raw_response)
            return intent, entities

        except Exception as e:
            log.error(f"NLU failed: {e}")
            return "UNKNOWN", {}  # Safe fallback

    def _ask_model(self, user_input: str) -> str:
        """
        Sends the input to Ollama and returns raw text response.
        """
        payload = {
            "model": self.model,
            "stream": False,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_input}
            ]
        }

        response = requests.post(self.url, json=payload, timeout=15)
        response.raise_for_status()

        data = response.json()
        raw_text = data["message"]["content"].strip()
        log.info(f"Model raw response: {raw_text}")

        return raw_text

    def _parse_response(self, raw: str) -> tuple[str, dict]:
        """
        Parses the JSON response from the model.
        Validates intent, extracts entities.
        """
        # Strip markdown fences just in case the model misbehaves
        clean = raw.strip().strip("```json").strip("```").strip()

        parsed = json.loads(clean)

        intent = parsed.get("intent", "UNKNOWN").upper()
        destination = parsed.get("destination", None)

        # If intent is not something we recognize → UNKNOWN
        if intent not in VALID_INTENTS:
            log.warning(f"Unexpected intent from model: '{intent}' → fallback to UNKNOWN")
            intent = "UNKNOWN"

        entities = {}
        if destination:
            destination = destination.lower()

            # remove common prefixes
            for prefix in ["lab", "room", "bureau"]:
                destination = destination.replace(prefix, "")

                destination = destination.strip()

                entities["destination"] = destination

        return intent, entities
    