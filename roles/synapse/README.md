# matrix-synapse

Deploy [synapse](https://github.com/matrix-org/synapse/), a matrix homeserver implementation in python, using ansible.

The role supports deployment both as systemd-services or as a docker container.

## Requirements

The following should be present on the target system when deploying synapse as a systemd service:
* `pip`
* `systemd`
* `rsyslogd`
* `logrotate`

If deploying synapse in a docker container, check that you have `docker` and the corresponding python-bindings (usually
`python3-docker`) installed.

## Role Variables

### Mandatory Variables

| Name                          | Type       | Description                                                                                 |
| :---                          | :---       | :---                                                                                        |
| `matrix_server_name`          | __string__ |                                                                                             |
| `matrix_synapse_tls_cert`     | __string__ | server's TLS certificate chain (_when `matrix_synapse_extra_config.no_tls` is set to true_) |
| `matrix_synapse_tls_key`      | __string__ | server's TLS key (_when `matrix_synapse_extra_config.no_tls` is set to true_)               |
| `matrix_synapse_report_stats` | __bool__   | Wether to report homeserver usage stats to matrix.org                                       |
| `matrix_synapse_pg_host`      | __string__ | postgresql server                                                                           |
| `matrix_synapse_pg_user`      | __string__ | postgresql user                                                                             |
| `matrix_synapse_pg_pass`      | __string__ | postgresql user's password                                                                  |
| `matrix_synapse_pg_db`        | __string__ | postgresql database                                                                         |

### Optional Variables

| Name                                | Default value                                                             | Description                                                                                                                   |
| :---                                | :---                                                                      | :---                                                                                                                          |
| `matrix_synapse_base_path`          | "/opt/synapse"                                                            |                                                                                                                               |
| `matrix_synapse_secrets_path`       | "{{ matrix_synapse_base_path }}/secrets"                                  |                                                                                                                               |
| `matrix_synapse_extra_config`       | _None_                                                                    | configuration parameters as given in the [synapse configuration file](https://github.com/matrix-org/synapse/tree/master/docs) |
| `matrix_synapse_dh_path`            | "{{ matrix_synapse_base_path }}/tls/{{ matrix_server_name }}.dh"          |                                                                                                                               |
| `matrix_synapse_public_baseurl`     | "https://{{ matrix_server_name }}"                                        |                                                                                                                               |
| `matrix_synapse_signing_key_path`   | "{{ matrix_synapse_base_path }}/ssl/{{ matrix_server_name }}.signing.key" |                                                                                                                               |
| `matrix_synapse_version`            | "v1.39.0"                                                                 |                                                                                                                               |
| `matrix_synapse_unstable`           | false                                                                     | when true, release candidate versions are deployed too                                                                        |
| `matrix_synapse_log_days_keep`      | 14                                                                        |                                                                                                                               |
| `matrix_synapse_deployment_method`  | pip                                                                       | Either pip or docker [¹](#footnote_1)                                                                                         |
| `matrix_synapse_supervision_method` | systemd                                                                   | Either systemd, runit or docker [¹](#footnote_1)                                                                              |
| `matrix_synapse_python_version`     | 3                                                                         | Default python version (2, 3) to be used                                                                                      |
| `matrix_synapse_redis_enabled`      | false                                                                     | If synapse should connect to redis (needed for workers)                                                                       |
| `matrix_synapse_redis_host`         | _None_                                                                    | host on which redis is running                                                                                                |
| `matrix_synapse_redis_port`         | 6379                                                                      | port on which redis is running                                                                                                |
| `matrix_synapse_redis_pass`         | _None_                                                                    | password to use to authentificate to redis                                                                                    |


### Worker control variables

| Name                                     | Default value | Description                                              |
| :---                                     | :---          | :---                                                     |
| `matrix_synapse_workers_enabled`         | `false`       | Enables workers and starts the replication listener      |
| `matrix_synapse_workers_client`          | `0`           | Amount of workers to deploy which serve the client API   |
| `matrix_synapse_workers_federation_in`   | `0`           | Amount of federation workers to deploy (inbound)         |
| `matrix_synapse_workers_federation_out`  | `0`           | Amount of federation sender workers to deploy (outbound) |
| `matrix_synapse_workers_media`           | `0`           | Amount of media-repo workers to deploy                   |
| `matrix_synapse_worker_push`             | `false`       | Enables a worker for pushes to sygnal/emal               |
| `matrix_synapse_worker_appservice`       | `false`       | Enables a worker to handle synapse->appservice traffic   |
| `matrix_synapse_worker_user_search`      | `false`       | Enable a worker to handle user_directory search          |
| `matrix_synapse_worker_replication_port` | `9003`        | Synapse replication port to use                          |
| `matrix_synapse_worker_metrics_enabled`  | `false`       | Enable metrics endpoint on each worker                   |
| `matrix_synapse_worker_metrics_port`     | `9101`        | Port on which metrics on each container can be reached   |

<a name="footnote_1">¹</a>: Docker must be used for both or neither deployment and supervision

## Dependencies

__None__.

## Example Playbook

```yaml
#TODO: Add example
```

## License

Apache 2.0

# Author Information

* Michael Kaye
* Jan Christian Grünhage
* Emmanouil Kampitakis
