# LiveKit WebRTC SFU

Deploys [LiveKit](https://docs.livekit.io/home/self-hosting/vm) and configures it, 
optionally in combination with a redis database.

## Requirements

A working docker installation `enable_docker: true` is required in order to generate 
the config files for LiveKit, as well as Let's Encrypt (`enable_lego: true`) and Traefik 
(`enable_traefik: true`).

## Variables

See [defaults](defaults/main.yml) for default variables.
The following mandatory variables have to be declared in the inventory on a per-host basis:

```yaml
enable_livekit: true
livekit_turnserver_domain: # the fqdn for the livekit TURN server
livekit_redis_enabled: # boolean value, defining if a redis database shall be created for livekit
livekit_jwt_service_container_enabled: # boolean value, for toggling the lk-jwt-service on / off
livekit_jwt_service_homeserver_allowlist: # optional list of domains or wildcard domains allowed to generate JWT tokens for livekit
```

A second domain record for the TURN server is needed, 
additionally to the `livekit_domain` (in the host_vars):

```yaml
livekit_domain: "{{ famedly_instance_domain }}"
livekit_turnserver_domain: "turn.dev.famedly.de"
```

Both domains must be included in the SAN list of the Let's Encrypt TLS
certificate (in the group_vars):

```yaml
lego_certificate:
  domains:
    - "{{ famedly_instance_domain }}"
    - "{{ livekit_turnserver_domain }}"
  email: "{{ famedly_acme_email }}"
```

Also, there needs to be a CNAME record for the additional 
domain (which can be found in group_vars/all/dns.yml):

```yaml
dns_cnames:
  - type: CNAME
    name: "{{ livekit_turnserver_domain }}."
    content: "{{ famedly_instance_domain }}."
    ttl: 3600
    when: "{{ enable_livekit|default(false) }}"
```

Additional `ufw` ACLs are defined in the group vars:

```yaml
famedly_firewall_per_host_allowlist:
  - service: webrtc-tcp
    port: 7881
    proto: tcp
  - service: turn-udp
    port: 3478
    proto: udp
  - service: webrtc-udp
    port: '50000:60000'
    proto: udp
```

"traefik" is required as a reverse proxy by setting `enable_traefik: true` (in the host_vars)
and including the correct router configuration in the group_vars:

```yaml
traefik_dynamic_extra_configs:
  - "livekit-router" # the livekit-router is always required for traefik to work properly
```

If one decides to use Redis in combination with LiveKit by setting `livekit_redis_enabled: true` as 
a host variable, the redis role will be imported as a task in the `livekit.yml` playbook.

The following variables are defined in the group_vars for that case:

```yaml
redis_config_bind_ip: "127.0.0.1"
redis_docker_networks:
  - name: host
```

The group_vars also must contain the port variables:

```yaml
livekit_ws_port: 7880
livekit_rtc_port: 7881
livekit_rtc_udp_port_start: 50000
livekit_rtc_udp_port_end: 60000
livekit_turns_port: 5349
livekit_turn_port: 3478
livekit_redis_port: 6379
livekit_jwt_service_external_port: 8888
```

The defaults are also used set the log level and manage log sampling (these can 
be overwritten using the group_vars or on a per-host basis):

```yaml
livekit_log_level: "info" # can be debug, info, warn or error
livekit_log_sample: true # 'true' avoids duplicate log entries and improves performance: https://github.com/uber-go/zap/blob/master/FAQ.md#why-sample-application-logs
```

## Dependencies

- famedly.base.redis

## Example Playbook

```yaml
- name: Deploy Livekit Server - an SFU for video calls
  hosts: [ livekit ]
  become: true
  tasks:
    - name: Set up a redis container for livekit
      ansible.builtin.import_role:
        name: famedly.base.redis
      when: livekit_redis_enabled | bool
    - name: Set up livekit and lk-jwt-service containers
      ansible.builtin.import_role:
        name: famedly.matrix.livekit
```

Author Information
------------------

[blueorca363](https://github.com/blueorca363)
