#!/bin/bash

source test-settings.sh

login_resp=` echo "{\"ANSIBLE_MODULE_ARGS\": {\"hs_url\": \"${HS_URL}\",\"user_id\": \"${USER_ID}\",\"password\": \"${PASSWORD}\"}}" | python matrix-login.py`

echo $login_resp

local_token=`echo $login_resp | jq --raw-output '.token'`

echo "{\"ANSIBLE_MODULE_ARGS\": {\"hs_url\": \"${HS_URL}\",\"token\": \"${local_token}\"}}" | python matrix-logout.py
