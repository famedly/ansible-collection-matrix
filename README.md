# Riot Webapp

Dowloads, verifies and deploys the riot webapplication

## Requirements

A webserver to server the application is required.
Additionally, gpg and dirmngr are required for the package verification

## Role Variables

### Mandatory Variables

__None__

### Optional Variables

| Name | Value | Description |
| :--- | :---  | :---        |
| riot_version | 1.1.2 | the riot version to be deployed |
| riot_webapp_dir | /opt/riot/ | location to upack the application |
| riot_config | __See (defaults)[defaults/main.yml] | Dictionary containing the webapp configuration see (riot documentation)[https://github.com/vector-im/riot-web#configjson] for details

## Dependencies

__None__

## Example Playbook

```yaml
- hosts: servers
  tasks:
    - name: install gpg and dirmngr
      apt:
        state: present
	name:
	  - gpg
	  - dirmngr
  roles:
    - role: ansible-riot-webapp
```

License
-------

MIT

Author Information
------------------

(madonius)[https://github.com/madonius]
