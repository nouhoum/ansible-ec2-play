# Bash Scripts

### data
This is an internal script that users need not know about.
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
**Usage**

Run individual Ansible scripts on the hosts with IDs listed in `hosts.ini` like this:

    bin/run [options] scriptName

Where `scriptName` is one of the Ansible scripts below.

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-d`         | Dry run, shows commands that would be executed                  |
| `-h`         | Display help                                                    |
| `-v`         | Increments verbose output (can be specified up to 3 times)      |
| `-x`         | Debug mode                                                      |

