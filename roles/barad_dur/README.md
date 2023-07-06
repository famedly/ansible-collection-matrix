# Barad-dûr role
Role to set up [Barad-dûr](https://gitlab.com/famedly/services/barad-dur), a matrix phone-home stats collector running in a  docker container.

## Usage
The database connection has to be defined in the playbook:
```yaml
barad_dur_database_user: "username"
barad_dur_database_password: "super_secret_password"
barad_dur_database_host: "serverhost"
barad_dur_database_name: "barad-dur"
```
The default scheme and port are set up for postgres, it can be changed with the `barad_dur_database_scheme` and `barad_dur_database_port` parameters respectively.


By default, all config files are placed in `/opt/barad-dur`.
