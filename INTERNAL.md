# Internal Documentation
This is implementation documentation.
End users should not need to read this.

## Bash Scripts
These are internal bash scripts that users need not know about.

### data
Maintains `$ANSIBLE_DATA_DIR/data/settings`.

**Options**

    -h        Display help
    -x        Debug mode

**Usage**

    data [options] operation instanceId [type parameters]

**Where**

| Option        | Description                         |
| ------------- | ----------------------------------- |
| `operation`   | One of `add`, `ignore` or `remove`. |
| `instanceId`  | The EC2 instance ID to consider.    |
| `type`        | Only required for the `add` operation. One of: `generic`, `playServer` or `postgresServer`. |
| `parameters`  | Only required for the `add` operation: All of: `userId`, `password`, `publicKey` and `keySignature` |

**Examples**

    data ignore i-234567
    data add    i-234568 generic userName password publicKey keySignature
    data remove i-234567

### Run
Runs individual Ansible scripts on the hosts with IDs listed in `hosts.ini`.

**Usage**

    bin/run [options] scriptName

**Where**

`scriptName` is one of the [Ansible scripts](README.md#ansible-scripts).

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-d`         | Dry run, shows commands that would be executed                  |
| `-h`         | Display help                                                    |
| `-v`         | Increments verbose output (can be specified up to 3 times)      |
| `-x`         | Debug mode                                                      |

## Ansible Scripts
Scripts may contain variables that need to be customized for your specific deployments.
Commonly modified variables have been factored into [`bin/custom.sample`](bin/custom.sample).
Make a copy of that file and save as `bin/custom` before modifying.

    cp bin/custom{.sample,}

The following Ansible scripts are available in the [`yaml` directory](yaml):

| Name          | Description                                                                                                             |
| ------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `bootstrap`   | Sets up an EC2 Ubuntu AMI.                                                                                              |
| `playEnv`     | Installs Play dependencies such as `pvm` and `java`.                                                                    |
| `playService` | Defines a system service for the Play application.                                                                      |
| `playDeploy`  | Clones a Play project from a Git repository and deploys it on the machine.                                              |
| `playLaunch`  | Launches the deployed Play app, killing the previous instance first if necessary.                                       |
| `postgresEnv` | Installs Postgres on a generic AWS EC2 instance, as an alternative to using an AWS RDS Postgres instance such as those created by `bin/rdsCreate`. Use `bin/psql` to restore the database before running `playLaunch` |

## hosts.ini
`hosts.ini` drives the Ansible scripts to provision various types of servers.
This file is automatically maintained through the bash scripts in the [`bin/`](bin) directory.
Once a server is provisioned by one of the [bash scripts](README.md#bash-scripts) it is automatically removed from `hosts.ini`.

`hosts.ini` contains 3 sections:

4. A section listing the EC2 domain names of generic EC2 servers to be provioned: `generic.domains`
5. A section listing the EC2 domain names of Play servers to be provioned: `playServer.domains`
6. A section listing the EC2 domain names of Postgres servers to be provioned: `postgresServer.domains`


````
[generic.domains]
ec2-54-196-57-227.compute-1.amazonaws.com
ec2-54-196-66-987.compute-1.amazonaws.com

[playServer.domains]
ec2-54-196-66-987.compute-1.amazonaws.com

[postgresServer.domains]
ec2-54-196-57-227.compute-1.amazonaws.com
````

Note that each entry in the `playServer.domains` and `postgresServer.domains` sections should also appear in the `generic.domains` section.

Implementation note: the internal [`bin/data`](#data) command automatically creates [`hosts.ini`](#hostsini) from information stored in `$ANSIBLE_DATA_DIR/data/settings`; 
it is automatically invoked by the [`bin/`](bin) scripts when creating a new server.
