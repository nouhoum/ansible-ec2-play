# EC2 Utilities

## ec2Create
Creates an EC2 instance and key pair if required.
The ID of the new EC2 instance is automatically added to `$ANSIBLE_DATA_DIR/data/settings` and `hosts.ini`.

**Usage**

    ec2Create [options] keyPairName classFQ amiId type userId password [description]

Where:

| Option        | Description                                                                                                               |
| ------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `keyPairName` | Key pair name, which will be created and stored in the `data/` directory if not already defined.                          |
| `classFQ`     | Is one of the [instance type values](http://aws.amazon.com/ec2/instance-types/#instance-details), for example: `t1.micro` |
| `amiId`       | AMI image ID listed in [general images](https://aws.amazon.com/marketplace/ref=mkt_ste_amis_redirect?b_k=291) and [Ubuntu images](http://cloud-images.ubuntu.com/releases/13.10/release/), for example: `ami-51274050` |
| `type`        | One of: generic, playServer or postgresServer. If not specified, this will be a generic server.                           |

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-c`         | Count of instances to launch                                    |
| `-d`         | Dry run, shows commands that would be executed                  |
| `-h`         | Display help                                                    |
| `-q`         | Quiet mode; suppress all output                                 |
| `-s string`  | Security group                                                  |
| `-w`         | Wait for the process to complete before returning               |
| `-x`         | Debug mode                                                      |
| `-z string`  | [Availability Zone](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html); defaults to `us-east-1c` |

**Examples**

Create a generic Ubuntu 13.10 micro image in the default availability zone with the default security group, and wait for the process to complete before returning.
Define key pair `testKey` if it does not already exist.

    ec2Create -w testServer testKey t1.micro ami-4b143122 generic fred yabbadabbadoo 'Just for experimentation'"

Create a Play server using Ubuntu 13.10 micro image in `us-east-1c`, and wait for the process to complete before returning:

    ec2Create -w testServer testKey t1.micro ami-4b143122 playServer fred yabbadabbadoo

Create a Postgres server using Ubuntu 13.10 micro image in `us-east-1c`, and wait for the process to complete before returning:

    ec2Create -w testServer testKey t1.micro ami-4b143122 postgresServer fred yabbadabbadoo

Create a server with Play and Postgres using Ubuntu 13.10 micro image in `us-east-1c`, and wait for the process to complete before returning:

    ec2Create -w testServer testKey t1.micro ami-4b143122 playServers postgresServer fred yabbadabbadoo

## ec2Delete
Deletes one or more EC2 instance(s).
Deleting instances multiple times will not cause an error.
This operation takes several minutes, during which time `ec2Ids` will continue to show that the instance(s) exist.
You can track the progress of the deletion process by running the `ec2Status` command repeatedly.
IDs of deleted EC2 instances are automatically removed from `hostIds`.

**Usage**

    ec2Delete [options] instanceId...

**Where**

| Option        | Description                                                                                                               |
| ------------- | ------------------------------------------------------------------------------------------------------------------------- |
| `instanceId`  | EC2 instance ID(s). Separate multiple instance IDs with spaces.                                                           |

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-d`         | Dry run, shows commands that would be executed                  |
| `-h`         | Display help                                                    |
| `-w`         | Wait for the process to complete before returning               |
| `-x`         | Debug mode                                                      |

**Example**

Do a dry run of deleting an EC2 instance.

    ec2Delete -d i-7cf09e18

## ec2InstanceId
Given an EC2 domain name or IP address, returns the EC2 instance id.
Domain name must be of the form: `ec2-54-196-57-227.compute-1.amazonaws.com`

**Usage**

    ec2InstanceId [options] id

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-h`         | Display help                                                    |
| `-i`         | return IP address                                               |
| `-n`         | return DNS name                                                 |
| `-x`         | Debug mode                                                      |

**Examples**

````
ec2InstanceId i-7cf09e18
aws ec2 stop-instances --instance-ids
aws ec2 start-instances --instance-ids
````

## ec2Ids
Displays all EC2 instance ids for this AWS account.

**Usage**

    ec2Ids [options]

**Options**

| Option       | Description                                                                          |
| ------------ | ------------------------------------------------------------------------------------ |
| `-g group`   | Only show IDs for the specified group (ec2Instances, playServers or postgresServers) |
| `-h`         | Display help                                                                         |
| `-x`         | Debug mode                                                                           |

## ec2Info
Given an EC2 instance id, return the IP address, domain name or status.

**Usage**

    ec2Info [options] instanceIds

`instanceIds` are a space-delimited list of zero or more EC2 instance IDs.
If an empty list is provided then there is no output and no error.
Nonexistant instanceIDs are quietly ignored.

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-e`         | Return server description                                       |
| `-h`         | Display help                                                    |
| `-i`         | Return IP address (no output if the instance is stopped)        |
| `-n`         | Return DNS name (no output if the instance is stopped)          |
| `-s`         | Return status (running or stopped)                              |
| `-x`         | Debug mode                                                      |

## ec2InstanceId
Given an EC2 domain name or IP address, returns the EC2 instance id.
Domain name must be of the form: `ec2-54-196-57-227.compute-1.amazonaws.com`.

**Usage**

    ec2InstanceId [options] id

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-h`         | Display help                                                    |
| `-i`         | return IP address                                               |
| `-n`         | return DNS name                                                 |
| `-x`         | Debug mode                                                      |

**Examples**

````
ec2InstanceId i-7cf09e18
aws ec2 stop-instances --instance-ids
aws ec2 start-instances --instance-ids
````

## ec2Status
Returns the run status of the EC2 instance with the specified `instanceId`.
Values returned are: `pending`, `running`, `stopping`, `stopped` and `terminated`.

**Usage**

    ec2Status instanceId

## ec2Start
Starts the EC2 instances with the specified `instanceId`s.

**Usage**

    ec2Start [options] instanceIds

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-h`         | Display help                                                    |
| `-w`         | Wait for the process to complete before returning               |
| `-x`         | Debug mode                                                      |

## ec2Stop
Stops the EC2 instances with the specified `instanceId`s.

**Usage**

    ec2Stop [options] instanceIds

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-h`         | Display help                                                    |
| `-w`         | Wait for the process to complete before returning               |
| `-x`         | Debug mode                                                      |
