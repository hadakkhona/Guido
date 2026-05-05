import logging
from brain.navigation_map import NavigationMap, ROOMS

log = logging.getLogger(__name__)


class PersonLookup:

    def __init__(self):
        self.nav_map = NavigationMap()

        # -------------------------
        # NAME → ROOM ID
        # (based on your floor plan)
        # -------------------------
        self.people = {

            # Top row
            "alae": "1.39",
            "youssef": "1.38",
            "mephtha": "1.33",
            "nisrine": "1.32",
            "sara": "1.31",
            "hiba": "1.29",
            "oumaima": "1.28",
            "badr": "1.27",
            "taha": "1.26",

            # Right corridor
            "masrour": "1.15",
            "abibaw": "1.12",
            "mezzan": "1.11",
            "abderrahmane": "1.10",
            "mehdaoui": "1.07",
            "adamo": "1.06",
            "zineddine": "1.04",

            # Left side
            "loubna": "1.46",
            "asmae": "1.48",
            "hafid": "1.49",
            "taha left": "1.51",
            "abdellah": "1.52",
            "dir el hilali": "1.55",
            "khaoula": "1.57",

            # Bottom row (directors / profs)
            "meriem": "1.66",

            # Top right
            "saidou": "1.19",
            "mouha": "1.16",
        }

    def find_person(self, query: str) -> dict | None:
        """
        Resolve a person's name to a navigation target.
        """
        query = query.lower().strip()

        # direct match
        if query in self.people:
            room_id = self.people[query]
            return self.nav_map.find(room_id)

        # fuzzy / partial match
        for name, room_id in self.people.items():
            if query in name or name in query:
                return self.nav_map.find(room_id)

        log.warning(f"No person match for: '{query}'")
        return None

    def list_people(self) -> list:
        return list(self.people.keys())