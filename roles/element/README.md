# Element Web App

Dowloads, verifies and deploys the element web application and places into a
webroot, or runs it as a container. Writes config files, with optional per
domain configuration.

## Requirements

A webserver to serve the application is required if webroot installation mode is
used, otherwise docker for running the container.

In case of the webroot installation mode, gpg and dirmngr are required for the
package verification.

## Role Variables

See [defaults](defaults/main.yml) for optional variables. There are no mandatory
variables.

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
    - role: element
```

License
-------

MIT

Author Information
------------------

[madonius](https://github.com/madonius)
[jcgruenhage](https://jcg.re)
