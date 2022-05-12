import json
import secrets
import string
from copy import deepcopy
from typing import Any, Optional, Union
from typing import Dict


class RoomEvents:
    M_ROOM_CREATE = {
        "content": {
            "creator": "@example:localhost",
        },
        "sender": "@example:localhost",
        "state_key": "",
        "type": "m.room.create"
    }
    M_ROOM_MEMBER = {
        "content": {
            "membership": "join"
        },
        "membership": "join",
        "sender": "@example:localhost",
        "state_key": "@example:localhost",
        "type": "m.room.member"
    }
    # This is not to spec!
    M_ROOM_DUMMY = {
        "content": {
            "dummy": "I'm a test message"
        },
        "sender": "@example:localhost",
        "state_key": "@example:localhost",
        "type": "m.room.dummy"
    }


class RoomSimulator:
    INITIAL_DATA = {'rooms': {}, 'room_directory': {}}

    def __init__(self, data: str = json.dumps(INITIAL_DATA)):
        try:
            self.data = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            self.data = self.INITIAL_DATA

    def random_event_id(self):
        return ''.join(secrets.choice(string.ascii_uppercase + string.digits) for i in range(64))

    def send_event(self, room_id: str, event: Dict[str, Any]) -> Dict[str, Any]:
        event['event_id'] = self.random_event_id()
        for e in self.get_events(room_id):
            if e['type'] == event['type'] and e['state_key'] == event['state_key']:
                event['replaces_state'] = e['event_id']
        self.add_event(room_id=room_id, event=event)
        return event

    def get_events(self, room_id: str) -> Dict[str, Any]:
        return self.data['rooms'][room_id]

    def add_event(self, room_id: str, event: Dict[str, Any]) -> Dict[str, Any]:
        return self.data['rooms'][room_id].append(event)

    def get_state_event(self, room_id: str, event_type: str, state_key: str) -> Union[None, Dict[str, Any]]:
        events = list[Dict[str, Any]]()
        for e in self.get_events(room_id):
            if e['type'] == event_type and e['state_key'] == state_key:
                events.append(e)
        if len(events) > 0:
            return events[-1]
        return None

    def add_room(self, room_id: str, alias: Optional[str] = None):
        self.data['rooms'][room_id] = []
        if alias is not None:
            self.data['room_directory'][alias] = room_id
        return room_id

    def resolve_alias(self, alias: str) -> str:
        return self.data['room_directory'].get(alias, None)

    def export(self) -> str:
        return json.dumps(self.data)

    # Matrix Tasks

    def create_room(self, alias: Optional[str] = None):
        room_id = '!' + ''.join(
            secrets.choice(string.ascii_uppercase + string.digits) for i in range(10)) + ':matrix.example.tld'
        self.add_room(room_id, alias)
        return room_id

    # Matrix Events

    def m_room_create(self, room_id: str, creator: str) -> Dict[str, Any]:
        data = deepcopy(RoomEvents.M_ROOM_CREATE)
        data['content']['creator'] = creator
        data['sender'] = creator
        return self.send_event(room_id=room_id, event=data)

    def m_room_member(self,
                      room_id: str,
                      membership: str,
                      sender: str,
                      state_key: str) -> Dict[str, Any]:
        data = deepcopy(RoomEvents.M_ROOM_MEMBER)
        data['content']['membership'] = membership
        data['membership'] = membership
        data['sender'] = sender
        data['state_key'] = state_key
        return self.send_event(room_id=room_id, event=data)
