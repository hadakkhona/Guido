# brain/navigation_map.py — EIDIA Floor 1 Navigation Map
# Room types: LAB, BUREAU, SERVICE, AUTRE
# ArUco marker IDs are placed at every junction and room entrance
# Paths are sequences of (marker_id, action) tuples

import logging

log = logging.getLogger(__name__)


# ----------------------------
# ArUco Marker Positions
# (Physical placement plan)
# ----------------------------
#
#  [ENTRANCE] → M01
#
#  Bottom corridor:
#  M01 → M02 → M03 → M04 → M05 → M06
#                              ↑
#                         right corridor:
#                    M07 → M08 → M09 → M10
#
#  Top corridor:
#  M11 → M12 → M13 → M14 → M15
#
#  Left corridor:
#  M16 → M17 → M18 → M19
#
# Each room entrance has its own marker
# ----------------------------


ROOMS = {

    # -------------------------
    # LABS — Laboratoire / Salle de TP
    # -------------------------
    "1.02": {"name": "Lab 1.02",
            "type": "LAB",
            "aliases": ["lab 1.02",
            "salle 1.02",
            "laboratoire 1.02"],
            "marker_id": 102,
            "path_key": "bottom_right"
            },

    "1.03": {"name": "Lab 1.03",
            "type": "LAB",
            "aliases": ["lab 1.03",
            "salle 1.03",
            "laboratoire 1.03"],
            "marker_id": 103,
            "path_key": "bottom_right"
            },

    "1.30": {"name": "Lab 1.30",
            "type": "LAB",
            "aliases": ["lab 1.30",
            "salle 1.30",
            "laboratoire 1.30"],
            "marker_id": 130,
            "path_key": "top_corridor"
            },

    "1.47": {"name": "Lab 1.47",
            "type": "LAB",
            "aliases": ["lab 1.47",
            "salle 1.47"],
            "marker_id": 147,
            "path_key": "left_corridor"
            },

    "1.50": {"name": "Lab 1.50",
            "type": "LAB",
            "aliases": ["lab 1.50",
            "salle 1.50"],
            "marker_id": 150,
            "path_key": "left_corridor"
            },

    "1.65": {"name": "Lab 1.65",
            "type": "LAB",
            "aliases": ["lab 1.65",
            "salle 1.65"],
            "marker_id": 165,
            "path_key": "bottom_corridor"
            },

    "1.70": {"name": "Lab 1.70",
            "type": "LAB",
            "aliases": ["lab 1.70",
            "salle 1.70"],
            "marker_id": 170,
            "path_key": "bottom_corridor"
            },

    "1.73": {"name": "Lab 1.73",
            "type": "LAB",
            "aliases": ["lab 1.73",
            "salle 1.73"],
            "marker_id": 173,
            "path_key": "bottom_corridor"
            },

    "1.82": {"name": "Lab 1.82",
            "type": "LAB",
            "aliases": ["lab 1.82",
            "salle 1.82"],
            "marker_id": 182,
            "path_key": "bottom_right"
            },


    # -------------------------
    # BUREAUX — Offices
    # -------------------------
    # Left side
    "1.46": {
        "name": "Bureau 1.46",
        "type": "BUREAU",
        "aliases": ["1.46"],
        "marker_id": 146,
        "path_key": "left_corridor"
        },
    "1.48": {
        "name": "Bureau 1.48",
        "type": "BUREAU",
        "aliases": ["1.48"],
        "marker_id": 148,
        "path_key": "left_corridor"
        },
    "1.49": {
        "name": "Bureau 1.49",
        "type": "BUREAU",
        "aliases": ["1.49"],
        "marker_id": 149,
        "path_key": "left_corridor"
        },
    "1.51": {
        "name": "Bureau 1.51",
        "type": "BUREAU",
        "aliases": ["1.51"],
        "marker_id": 151,
        "path_key": "left_corridor"
        },
    "1.52": {
        "name": "Bureau 1.52",
        "type": "BUREAU",
        "aliases": ["1.52"],
        "marker_id": 152,
        "path_key": "left_corridor"
        },
    "1.53": {
        "name": "Bureau 1.53",
        "type": "BUREAU",
        "aliases": ["bureau 1.53",
        "office 1.53"],
        "marker_id": 153,
        "path_key": "left_corridor"
        },
    "1.54": {
        "name": "Bureau 1.54",
        "type": "BUREAU",
        "aliases": ["bureau 1.54",
        "office 1.54"],
        "marker_id": 154,
        "path_key": "left_corridor"
        },
    "1.58": {
        "name": "Bureau 1.58",
        "type": "BUREAU",
        "aliases": ["bureau 1.58",
        "office 1.58"],
        "marker_id": 158,
        "path_key": "left_corridor"
        },

    # Bottom corridor
    "1.62": {
        "name": "Bureau 1.62",
        "type": "BUREAU",
        "aliases": ["bureau 1.62",
        "office 1.62"],
        "marker_id": 162,
        "path_key": "bottom_corridor"
        },
    "1.63": {
        "name": "Bureau 1.63",
        "type": "BUREAU",
        "aliases": ["bureau 1.63",
        "office 1.63"],
        "marker_id": 163,
        "path_key": "bottom_corridor"
        },
    "1.64": {
        "name": "Bureau 1.64",
        "type": "BUREAU",
        "aliases": ["bureau 1.64",
        "office 1.64"],
        "marker_id": 164,
        "path_key": "bottom_corridor"
        },
    "1.66": {
        "name": "Bureau 1.66",
        "type": "BUREAU",
        "aliases": ["1.66"],
        "marker_id": 166,
        "path_key": "bottom_corridor"
        },
    "1.67": {
        "name": "Bureau 1.67",
        "type": "BUREAU",
        "aliases": ["1.67"],
        "marker_id": 167,
        "path_key": "bottom_corridor"
        },
    "1.68": {
        "name": "Bureau 1.68",
        "type": "BUREAU",
        "aliases": ["1.68"],
        "marker_id": 168,
        "path_key": "bottom_corridor"
        },
    "1.69": {
        "name": "Bureau 1.69",
        "type": "BUREAU",
        "aliases": ["1.69"],
        "marker_id": 169,
        "path_key": "bottom_corridor"
        },
    "1.71": {
        "name": "Bureau 1.71",
        "type": "BUREAU",
        "aliases": ["1.71"],
        "marker_id": 171,
        "path_key": "bottom_corridor"
        },
    "1.72": {
        "name": "Bureau 1.72",
        "type": "BUREAU",
        "aliases": ["1.72"],
        "marker_id": 172,
        "path_key": "bottom_corridor"
        },
    "1.74": {
        "name": "Bureau 1.74",
        "type": "BUREAU",
        "aliases": ["1.74"],
        "marker_id": 174,
        "path_key": "bottom_corridor"
        },
    "1.75": {
        "name": "Bureau 1.75",
        "type": "BUREAU",
        "aliases": ["1.75"],
        "marker_id": 175,
        "path_key": "bottom_corridor"
        },
    "1.77": {
        "name": "Bureau 1.77",
        "type": "BUREAU",
        "aliases": ["1.77"],
        "marker_id": 177,
        "path_key": "bottom_corridor"
        },

    # Right corridor
    "1.04": {
        "name": "Bureau 1.04",
        "type": "BUREAU",
        "aliases": ["1.04"],
        "marker_id": 104,
        "path_key": "right_corridor"
        },
    "1.05": {
        "name": "Bureau 1.05",
        "type": "BUREAU",
        "aliases": ["1.05"],
        "marker_id": 105,
        "path_key": "right_corridor"
        },
    "1.06": {
        "name": "Bureau 1.06",
        "type": "BUREAU",
        "aliases": ["1.06"],
        "marker_id": 106,
        "path_key": "right_corridor"
        },
    "1.07": {
        "name": "Bureau 1.07",
        "type": "BUREAU",
        "aliases": ["1.07"],
        "marker_id": 107,
        "path_key": "right_corridor"
        },
    "1.08": {
        "name": "Bureau 1.08",
        "type": "BUREAU",
        "aliases": ["1.08"],
        "marker_id": 108,
        "path_key": "right_corridor"
        },
    "1.10": {
        "name": "Bureau 1.10",
        "type": "BUREAU",
        "aliases": ["1.10"],
        "marker_id": 110,
        "path_key": "right_corridor"
        },
    "1.11": {
        "name": "Bureau 1.11",
        "type": "BUREAU",
        "aliases": ["1.11"],
        "marker_id": 111,
        "path_key": "right_corridor"
        },
    "1.12": {
        "name": "Bureau 1.12",
        "type": "BUREAU",
        "aliases": ["1.12"],
        "marker_id": 112,
        "path_key": "right_corridor"
        },
    "1.13": {
        "name": "Bureau 1.13",
        "type": "BUREAU",
        "aliases": ["1.13"],
        "marker_id": 113,
        "path_key": "right_corridor"
        },

    # Top corridor
    "1.23": {
        "name": "Bureau 1.23",
        "type": "BUREAU",
        "aliases": ["1.23"],
        "marker_id": 123,
        "path_key": "top_corridor"
        },
    "1.25": {
        "name": "Bureau 1.25",
        "type": "BUREAU",
        "aliases": ["1.25"],
        "marker_id": 125,
        "path_key": "top_corridor"
        },
    "1.26": {
        "name": "Bureau 1.26",
        "type": "BUREAU",
        "aliases": ["1.26"],
        "marker_id": 126,
        "path_key": "top_corridor"
        },
    "1.27": {
        "name": "Bureau 1.27",
        "type": "BUREAU",
        "aliases": ["1.27"],
        "marker_id": 127,
        "path_key": "top_corridor"
        },
    "1.28": {
        "name": "Bureau 1.28",
        "type": "BUREAU",
        "aliases": ["1.28"],
        "marker_id": 128,
        "path_key": "top_corridor"
        },
    "1.29": {
        "name": "Bureau 1.29",
        "type": "BUREAU",
        "aliases": ["1.29"],
        "marker_id": 129,
        "path_key": "top_corridor"
        },
    "1.31": {
        "name": "Bureau 1.31",
        "type": "BUREAU",
        "aliases": ["1.31"],
        "marker_id": 131,
        "path_key": "top_corridor"
        },
    "1.32": {
        "name": "Bureau 1.32",
        "type": "BUREAU",
        "aliases": ["1.32"],
        "marker_id": 132,
        "path_key": "top_corridor"
        },
    "1.33": {
        "name": "Bureau 1.33",
        "type": "BUREAU",
        "aliases": ["1.33"],
        "marker_id": 133,
        "path_key": "top_corridor"
        },

    # -------------------------
    # SERVICES
    # -------------------------
    "1.09": {
        "name": "Archive 1.09",
        "type": "SERVICE",
        "aliases": ["archive",
        "1.09",
        "archives"],
        "marker_id": 109,
        "path_key": "right_corridor"
        },
    "1.20": {
        "name": "Convivialité 1.20",
        "type": "SERVICE",
        "aliases": ["conviv",
        "convivialite",
        "1.20"],
        "marker_id": 120,
        "path_key": "top_right"
        },
    "1.24": {
        "name": "Salle de Réunion 1.24",
        "type": "SERVICE",
        "aliases": ["reunion 1.24"],
        "marker_id": 124,
        "path_key": "top_corridor"
        },
    "1.35": {
        "name": "Salle de Réunion 1.35",
        "type": "SERVICE",
        "aliases": ["reunion 1.35",
        "reunion"],
        "marker_id": 135,
        "path_key": "top_corridor"
        },

    # -------------------------
    # AUTRES
    # -------------------------
    "1.16": {
        "name": "Bureau 1.16",
        "type": "BUREAU",
        "aliases": ["1.16"],
        "marker_id": 116,
        "path_key": "top_right"
        },
    "1.17": {
        "name": "Salle 1.17",
        "type": "AUTRE",
        "aliases": ["1.17"],
        "marker_id": 117,
        "path_key": "top_right"
        },
    "1.18": {
        "name": "Salle 1.18",
        "type": "AUTRE",
        "aliases": ["1.18"],
        "marker_id": 118,
        "path_key": "top_right"
        },
    "1.19": {
        "name": "Bureau 1.19",
        "type": "BUREAU",
        "aliases": ["1.19"],
        "marker_id": 119,
        "path_key": "top_right"
        },
    "1.83": {
        "name": "Salle 1.83",
        "type": "AUTRE",
        "aliases": ["1.83"],
        "marker_id": 183,
        "path_key": "bottom_right"
        },
    "1.84": {
        "name": "Salle 1.84",
        "type": "AUTRE",
        "aliases": ["1.84"],
        "marker_id": 184,
        "path_key": "bottom_right"
        },
}



# ----------------------------
# ArUco Path Sequences
# Each path = list of {"marker": int,"command": str}
# Commands sent to Arduino Mega via SerialBridge
# ----------------------------

PATHS = {

    "bottom_corridor": [
        {"marker": 1,  "command": "GO_STRAIGHT"},
        {"marker": 2,  "command": "GO_STRAIGHT"},
        {"marker": 3,  "command": "GO_STRAIGHT"},
    ],

    "bottom_right": [
        {"marker": 1,  "command": "GO_STRAIGHT"},
        {"marker": 2,  "command": "GO_STRAIGHT"},
        {"marker": 6,  "command": "TURN_RIGHT"},
        {"marker": 7,  "command": "GO_STRAIGHT"},
    ],

    "right_corridor": [
        {"marker": 1,  "command": "GO_STRAIGHT"},
        {"marker": 6,  "command": "TURN_RIGHT"},
        {"marker": 7,  "command": "GO_STRAIGHT"},
        {"marker": 8,  "command": "GO_STRAIGHT"},
    ],

    "top_right": [
        {"marker": 1,  "command": "GO_STRAIGHT"},
        {"marker": 6,  "command": "TURN_RIGHT"},
        {"marker": 9,  "command": "GO_STRAIGHT"},
        {"marker": 10,
        "command": "TURN_LEFT"},
    ],

    "top_corridor": [
        {"marker": 1,  "command": "GO_STRAIGHT"},
        {"marker": 2,  "command": "GO_STRAIGHT"},
        {"marker": 11, "command": "TURN_LEFT"},
        {"marker": 12, "command": "GO_STRAIGHT"},
        {"marker": 13, "command": "GO_STRAIGHT"},
    ],

    "left_corridor": [
        {"marker": 1,  "command": "GO_STRAIGHT"},
        {"marker": 2,  "command": "GO_STRAIGHT"},
        {"marker": 16, "command": "TURN_LEFT"},
        {"marker": 17, "command": "GO_STRAIGHT"},
    ],
}


class NavigationMap:

    def find(self, destination: str) -> dict | None:
        """
        Tries to match user's destination string to a known room.
        Returns full room dict or None if not found.
        """
        destination = destination.lower().strip()

        for room_id, room in ROOMS.items():
            # Direct room number match
            if destination == room_id:
                return self._build_result(room)

            # Alias match
            if destination in room["aliases"]:
                return self._build_result(room)

            # Partial match — "lab 1.0" matches "lab 1.02"
            for alias in room["aliases"]:
                if destination in alias or alias in destination:
                    return self._build_result(room)

        log.warning(f"No match found for destination: '{destination}'")
        return None

    def _build_result(self, room: dict) -> dict:
        """
        Builds the result dict that DecisionMaker will use.
        """
        path = PATHS.get(room["path_key"], [])
        return {
            "name":    room["name"],
            "type":    room["type"],
            "command": f"GOTO_{room['marker_id']}",
            "path":    path
        }

    def list_all(self) -> list:
        """
        Returns all available destinations — useful for debugging
        or if you want Guido to say 'I can guide you to...'
        """
        return [room["name"] for room in ROOMS.values()]