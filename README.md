# Ansible Collection - `famedly.matrix`

![Matrix](https://img.shields.io/matrix/ansible-famedly:matrix.org)

## Modules

This collection contains modules for managing matrix rooms
and more via ansible. They can modify room membership,
aliases, server signing keys and even send messages into
rooms from within ansible.

- [`matrix_login` (source)](plugins/modules/matrix_login.py):
  Create an access token for a matrix account.
- [`matrix_login` (source)](plugins/modules/matrix_login.py):
  Create an access token for a matrix account.
  Logs in with user and password to obtain a matrix access token
- [`matrix_uia_login` (source)](plugins/modules/matrix_uia_login.py):
  Logs in with user and password to obtain a matrix access token, while
  implementing [user-interactive authentication](https://spec.matrix.org/unstable/client-server-api/#user-interactive-authentication-api)
  on the `_matrix/client/r0/login` endpoint (see [MSC2835](https://github.com/Sorunome/matrix-doc/blob/soru/uia-on-login/proposals/2835-uia-on-login.md)).
- [`matrix_logout` (source)](plugins/modules/matrix_logout.py):
  Invalidates an access token.
- [`matrix_notification` (source)](plugins/modules/matrix_notification.py):
  Sends a message to a matrix room.
- [`matrix_room` (source)](plugins/modules/matrix_room.py):
  Idempotently joins/creates a room with a given alias.
- [`matrix_state` (source)](plugins/modules/matrix_state.py):
  Can be used to set matrix state events to a room.
- [`matrix_member` (source)](plugins/modules/matrix_member.py):
  Can be used to manipulate matrix room membership.
- [`matrix_signing_key` (source)](plugins/modules/matrix_signing_key.py):
  Creates a server signing key.
- [`synapse_register` (source)](plugins/modules/synapse_register.py):
  Registers a user using synapse's admin API.
- [`synapse_ratelimit` (source)](plugins/modules/synapse_ratelimit.py):
  Gets / Sets / Deletes a (local) users ratelimits

For more information on how to use the modules to manage matrix rooms
via ansible, the [README in `./plugins/modules/`](plugins/modules/README.md)
provides more detailed information and an example playbook.

## Roles
In addition to the modules, this role *also* contains a few roles for
deploying commonly used matrix services:

- [`synapse`](roles/synapse/README.md): synapse, a reference matrix homeserver
  implementation in python, maintained mostly by element.
- [`element`](roles/element/README.md): element-web, a reference matrix client implementation,
  able to run in the browser, maintained by element.
- [`hedwig`](roles/hedwig/README.md): Hedwig, a push-gateway server alternative
  to `sygnal`, developed by Famedly.
- [`barad-dur`](roles/barad-dur/README.md): Barad-dûr, a matrix phone-home stats collector alternative, developed by Famedly.
