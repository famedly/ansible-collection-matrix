#!/bin/bash

source test-settings.sh

notification_resp=` echo "{\"ANSIBLE_MODULE_ARGS\": {\"hs_url\": \"${HS_URL}\", \"token\": \"${TOKEN}\", \"room_id\": \"${ROOM_ID}\", \"msg_plain\": \"**Hello, World!**\", \"msg_html\": \"<b>Hello, World!</b>\"}}" | python matrix_notification.py`

echo $notification_resp
