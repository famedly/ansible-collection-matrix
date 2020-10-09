# Ansible Collection - famedly.matrix

## Modules
This collection contains a few modules for managing matrix rooms and
servers, as well as sending notifications from ansible to matrix.

 - **matrix\_login**: Create an access token for a matrix account.
 - **matrix\_logout**: Invalidates an access token.
 - **matrix\_notification**: Sends a message to a matrix room.
 - **matrix\_room**: Idempotently joins/creates a room with a given
   alias.
 - **matrix\_state**: Ensures room state has a given content.
 - **matrix\_member**: Ensures room memberships are correct.
 - **matrix\_signing\_key**: Creates a server signing key.
 - **synapse\_register**: Registers a user using synapse's admin API.

You can find more information and a sample playbook for these modules in the
README in `./plugins/modules/`

## Roles
In addition to the modules, this role *also* contains a few roles for
deploying commonly used matrix services:

 - **synapse**: Homeserver, this is where your accounts live.
 - **element**: Web client, for using your accounts.

For details on using these, look at the README.md in the respective
role directory.
