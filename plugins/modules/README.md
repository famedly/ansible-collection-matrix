# Matrix Ansible Modules

These are a few ansible modules for working with matrix rooms.

## Requirements

 - **nio**: The modules require matrix-nio to be required on the target. Some bugs and missing features were found during the development of these modules, which have been fixed in the case of bugs and implemented in the case of missing features. Until they are merged upstream, you have to install the matrix-nio library from source using https://github.com/poljar/matrix-nio/pull/102.
 - **Python >= 3.5**: The modules make extensive use of async/await, so only Python 3.5 or later are supported. These modules have only been tested with Python 3.8 so far.

## Example Playbook

```yaml
- hosts: localhost
  collections:
    - famedly.matrix
  gather_facts: false
  vars:
    matrix:
      homeserver: "https://example.org"
      user: "some_user"
      password: "s3cr3t"
      alias: "#module-tests:example.org"
      invitees:
        - '@another_user:example.org'
        - '@a_third_user:example.org'
  tasks:
    - synapse_register:
        hs_url: "{{ matrix.homeserver }}"
        user_id: "{{ matrix.user }}"
        password: "{{ matrix.password }}"
        admin: false
        shared_secret: "iqueok1zeengieW3ohcha0riePaigh9p"
    - matrix_login:
        hs_url: "{{ matrix.homeserver }}"
        user_id: "{{ matrix.user }}"
        password: "{{ matrix.password }}"
      register: login_result
    - matrix_room:
        hs_url: "{{ matrix.homeserver }}"
        token: "{{ login_result.token }}"
        alias: "{{ matrix.alias }}"
      register: room_result
    - matrix_state:
        hs_url: "{{ matrix.homeserver }}"
        token: "{{ login_result.token }}"
        room_id: "{{ room_result.room_id }}"
        event_type: "m.room.name"
        state_key: ""
        content:
          name: "test room name"
      register: state_result
    - matrix_member:
        hs_url: "{{ matrix.homeserver }}"
        token: "{{ login_result.token }}"
        room_id: "{{ room_result.room_id }}"
        user_ids: "{{ matrix.invitees }}"
        state: "member"
        exclusive: False
      register: membership_changes
    - matrix_notification:
        hs_url: "{{ matrix.homeserver }}"
        token: "{{ login_result.token }}"
        room_id: "{{ room_result.room_id }}"
        msg_plain: "Updated memberships: {{ membership_changes | to_json }}"
        msg_html: "Updated memberships: {{ membership_changes | to_json }}"
      when: membership_changes.changed
    - matrix_logout:
        hs_url: "{{ matrix.homeserver }}"
        token: "{{ login_result.token }}"
```
