# Ansible Collection - `famedly.matrix`

![Matrix](https://img.shields.io/matrix/ansible-famedly:matrix.org)

## Modules

This collection contains modules for managing matrix rooms
and more via ansible. They can modify room membership,
aliases and server signing keys from within ansible.

- [`matrix_login` (source)](plugins/modules/matrix_login.py):
  Create an access token for a matrix account.
- [`matrix_login` (source)](plugins/modules/matrix_login.py):
  Create an access token for a matrix account.
  Logs in with user and password to obtain a matrix access token
- [`matrix_logout` (source)](plugins/modules/matrix_logout.py):
  Invalidates an access token.
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

For more information on how to use the modules to manage matrix rooms
via ansible, the [README in `./plugins/modules/`](plugins/modules/README.md)
provides more detailed information and an example playbook.

## Roles
In addition to the modules, this role *also* contains a few roles for
deploying commonly used matrix services:

- [`synapse`](roles/synapse/README.md): synapse, a reference matrix homeserver
  implementation in python, maintained mostly by element.
- [`hedwig`](roles/hedwig/README.md): Hedwig, a push-gateway server alternative
  to `sygnal`, developed by Famedly.
- [`barad_dur`](roles/barad_dur/README.md): Barad-dûr, a matrix phone-home stats collector alternative, developed by Famedly.
