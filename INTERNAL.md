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
| `-v`         | Increments verbose output (can be specified up to 4 times)      |
| `-x`         | Debug mode                                                      |

## data/settings
This file contiains configuration information about all the servers created from the `ec2Create` and `rdsCreate` commands.
It is updated by the `provision` command and is referred to by the `psql` and `ec2ssh` commands. Here is a sample file:

````
[
  {
    "instanceId": "i-345678",
    "user": "myUserName",
    "password": "myPassword",
    "publicKey": "myPublicKey",
    "keySignature": "myKeySignature",
    "description": "Production",
    "types": [
      {"generic": "provisioned"},
      {"postgresServer": "notProvisionedYet"},
      {"playServer": "provisioned"}
    ]
  }
]
````
Three types of servers are handled: `generic`, `playServer` and `postgresServer`.
Each of these servers can have two states: `provisioned` and `notProvisioned`.
The `bin/provision` command creates `hosts.ini` and populates it with servers that are `notProvisioned` in the appropriate sections of that temporary file.

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
`hosts.ini` is a temporary file that drives the Ansible scripts to provision various types of servers.
This file is automatically created when the `bin/provision` bash script runs, and is deleted at the end of that script.

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

Implementation note: the internal [`bin/data`](#data) command automatically creates [`hosts.ini`](#hostsini) from information stored in `$ANSIBLE_DATA_DIR/data/settings`.

## EC2 Public Key Files
The file type for EC2 public key files is `pem` and it contains JSON.
Here is a sample file, which must be located in `$ANSIBLE_DATA_DIR/test.pem`, according to the `KeyName` property in the file:


````
{
    "KeyMaterial": "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEApA8k8RpLFMUqsjz8FioiUSedLL7+YkxnsR4Y8G6y8+zVPpwXTI7h4dkeTxVA\nUe+zKEu4y5yQytt9qRg9a4OWksqEgF0/PK2WcMxJyXMJcCP96ZD86rHv/lQrjxUsPh6LnhQYvRoO\nwBnW+QaevjBNPcXbyC8NBWmxUM8Yuuy8eW9V+82OqB6T81UhnZTbBdYxskUHjXNnGs91JBJWfMcz\nlujcrP39GDydO19kSS/Y+yS3FgvQocf31V20OmON71Egk+1+goVmdAWlpt39TmCoQ5vLn1R0Y+CP\nb8CJRir1VT7S1ksbKvLqiF2dbWuxVxpxiMiyfcgxt6NoXBdZARzVCwIDAQABAoIBAEPeoAG+RuFI\nz+j8oazpsVixcqxYNxSjVyJGuTp+ETon9+/20wyw73FnSMqemAVNjGhXKxPQqXXCZ7HUfVRFE72W\nWkpgSRDpHxt65+uW04i42woNGRRemFI2r+55a9wm9stmtPVGGmQOTIio3HMBuHKdr9aY4GIk3132\nztxFo5L4enwjElek+fvDz2SF0l9CbMxU8z6WPnscqeLnVmuY79+zdER2zMz9s51x4uXm664HyvjA\nTzP36eIOS0P6N4v1337bvEb6Up4zchWcpTPaknNIzFpYhC1KyC0iktHy0WrvQvhwkzEqz+2lmXIA\nd7e+47l07nUMj1GP5OB7Is94mEECgYEA1Z7WUgNhkK3TrfZy8VtBNAMe8cWOG6MvrNba5Ua4qQel\n1PBal/Xb/N+aD4j41NwKLPFv6ngVBmvDWaXISPEAMHktheI+LKluH+crdLOJXs5WhjhwibshX+xM\nmZVMDcwmtjjCzXJuqLHqovnIwUoWchlXSfeZzsdxO8UDNcXON0cCgYEAxJs7ib4gLfGabNnrr8GA\nGqCNpwIL2NzQ6So7DjpeWkjUGitF8SWaGwDYlxNdmfFyFEw8V+IsIIeqZK5jkHk93pxEllMqqDlG\nKi+oTzDc0TiVHmT0szwOhmIwocSby2GBbqcq+q//50M/eDoiNC8/afD8P7bzWYOA5mlNXV8n3h0C\ngYEAoSh9g83tMxsQkTNWL+OqYzTfiYKC3TLVas2EwmgCM/MDFoxlrDLdTf7a2VF6eAuw2Ysj5X3G\nTtvJur4pRW4buHYS8+hlA4im/gaGcDpqLk34VLYLoLy+RwGcIFnT0Kztn5dez2O/PCFNZLqQy9G6\n8UVQ5wqWzLsGIBNXgp/CHU0CgYAOKaSLUp/cz2exaa1ZttW0lVY+7p3N3HJMKZehecDsPgzRacab\nDXthcJkpoOKAQW1XWvqJ1igZm8xBfnJ7qNA1JgqmzYzoG2Abj91O/xUZGTtcuicKdkwRkCcysAgN\nCZQaVX56Go2Tqjt7PKzUF4c46XwyVsqG6zsw3esNy9oCXQKBgChsJxDfbMsFgsyuSygRZFGHJjYL\nq00uXeHRXfqGf2/OkbFBA6zhB9pPCWDIlBm43B/1VrULdVF5hN+MsptPUxS2tpy8JU3+9JrXCR8k\n0Ou8rpFSakGXxtClL9yN86qH3O3ngK0m2Zn2RJZZOe+1PUgLRYHKy9Fa8NYeQcWdGCmg\n-----END RSA PRIVATE KEY-----",
    "KeyName": "test",
    "KeyFingerprint": "d9:b0:0f:ec:85:cc:a9:15:19:be:0b:ac:e8:67:27:55:e0:a7:0d:b5"
}
````
