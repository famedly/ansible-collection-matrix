# `famedly.matrix.sygnal` ansible role (UNMAINTAINED)

This role installs sygnal, the reference matrix push gateway server.

## Role Variables

specify Apps with:
```yaml
sygnal_apps:
  - id: com.example.myapp
    type: apns
    apns_certfile: com.example.myApp_prod_APNS.pem

  - id: com.example.myotherapp
    type: gcm
    gcm_api_key: your_api_key_for_gcm
```

it is possible to use systemd and pip instead of docker, specify as follows:
```yaml
sygnal_supervision_method: systemd
sygnal_deployment_method: pip
```

CAUTION: this role is not tested with this variables set, probably it needs maintenace to work properly

You have to overide the db password in order to run sygnal
```yaml
sygnal_postgresql_password: "your database password here"
```

A complete list of all variables is in [`defaults/main.yml`](defaults/main.yml)

## License

AGPLv3

## Author Information

- Jan Christian Grünhage <jan.christian@gruenhage.xyz>
- Vincent Wilke <v.wilke@famedly.de>
