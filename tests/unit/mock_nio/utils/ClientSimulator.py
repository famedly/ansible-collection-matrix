import json
from typing import List


class ClientSimulator:
    INITIAL_DATA = {"rooms": []}

    def __init__(self, data: str = json.dumps(INITIAL_DATA)):
        try:
            self.data = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            self.data = self.INITIAL_DATA

    def export(self) -> str:
        return json.dumps(self.data)

    def join(self, room_id: str):
        self.data["rooms"].append(room_id)

    def get_joined_rooms(self) -> List[str]:
        return self.data["rooms"]
