#!/bin/bash

source test-settings.sh

state_resp=` echo "{\"ANSIBLE_MODULE_ARGS\": {\"hs_url\": \"${HS_URL}\", \"token\": \"${TOKEN}\", \"room_id\": \"${ROOM_ID}\", \"state_key\": \"\", \"event_type\": \"m.room.name\", \"content\": { \"name\": \"test room name\"}}}" | python matrix-state.py`

echo $state_resp
