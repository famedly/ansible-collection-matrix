# `famedly.matrix.room

Create and manage common room settings.

## Role Variables

### Mandatory
- `matrix_hs_url`: URL of the Matrix homeserver.
- `matrix_token`: Access token of the user that manages this room.
- `matrix_room_alias`: Full room alias of the room, including the server part.

### Optional
- `matrix_room_name`: Allows setting the room name.
- `matrix_room_topic`: Allows setting the room topic.
- `matrix_room_enable_encryption`: Allows enabling encryption for a room,
  defaults to false. **Once enabled this can't be disabled again.**
- `matrix_room_join_rule`: Allows setting the join rule for the room. Related
  to this, there is also `matrix_room_join_rules_restricted_allow` available.
  For details, look at
  https://spec.matrix.org/v1.5/client-server-api/#mroomjoin_rules.
- `matrix_room_additional_state`: Allows setting arbitrary additional state
  events for a room. Takes an array of dicts, with the relevant keys being
  `event_type`, `state_key` and `content`.

## License

AGPL-3.0-only

## Author Information

- `Jan Christian Grünhage <jan.christian@gruenhage.xyz>`
