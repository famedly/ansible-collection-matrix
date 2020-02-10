#!/bin/bash

source test-settings.sh

room_resp=` echo "{\"ANSIBLE_MODULE_ARGS\": {\"hs_url\": \"${HS_URL}\",\"token\": \"${TOKEN}\",\"alias\": \"${ROOM_ALIAS}\"}}" | python matrix-room.py`

echo $room_resp
