# Matrix Ansible Modules

This repo contains a few ansible modules for working with matrix rooms.

## Installation

To install these modules so that you can use them, put them into `~/.ansible/plugins/modules/` or for global installation, install them to `/usr/share/ansible/plugins/modules/`.

## Requirements

 - **nio:** The modules require matrix-nio to be required on the target. Some bugs and missing features were found during the development of these modules, which have been fixed in the case of bugs and implemented in the case of missing features. Until they are merged upstream, you have to install the matrix-nio library from source using https://github.com/poljar/matrix-nio/pull/102.
 - **Python >= 3.5:** The modules make extensive use of async/await, so only Python 3.5 or later are supported. These modules have only been tested with Python 3.8 so far.

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
