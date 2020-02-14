# Matrix Ansible Modules

This repo contains a few ansible modules for working with matrix rooms.

## Installation

To install these modules so that you can use them, put them into `~/.ansible/plugins/modules/` or for global installation, install them to `/usr/share/ansible/plugins/modules/`.

## Usage

For a usage example including all modules, look at the example playbook below.
```yaml
- hosts: localhost
  vars:
    matrix:
      homeserver: https://example.org
      user: username
      password: s3cr3t
      alias: '#some-alias:example.org'
      message: "Set room name in"
  tasks:
    - matrix-login:
        hs_url: "{{ matrix.homeserver }}"
        user_id: "{{ matrix.user }}"
        password: "{{ matrix.password }}"
      register: login_result
    - matrix-room:
        hs_url: "{{ matrix.homeserver }}"
        token: "{{ login_result.token }}"
        alias: "{{ matrix.alias }}"
      register: room_result
    - matrix-state:
        hs_url: "{{ matrix.homeserver }}"
        token: "{{ login_result.token }}"
        room_id: "{{ room_result.room_id }}"
        event_type: "m.room.name"
        state_key: ""
        content:
          name: "test room name"
      register: state_result
    - matrix-notification:
        hs_url: "{{ matrix.homeserver }}"
        token: "{{ login_result.token }}"
        room_id: "{{ room_result.room_id }}"
        msg_plain: "{{ matrix.message }} {{ state_result.event_id}}"
        msg_html: "{{ matrix.message }} {{ state_result.event_id}}"
      when: state_result.changed
    - matrix-logout:
        hs_url: "{{ matrix.homeserver }}"
        token: "{{ login_result.token }}"
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[AGPLv3](https://choosealicense.com/licenses/agpl-3.0/)
