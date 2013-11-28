# AWS command line toolkit Support for RDS
These features require the [AWS command-line toolkit](http://aws.amazon.com/developertools/2928). 
Documentation on the AWS RDS commands [here](http://docs.aws.amazon.com/AmazonRDS/latest/CommandLineReference/Welcome.html).

## rdsCreate
Creates a database server.
This operation takes several minutes, during which time the database is not available.

**Usage** 

    rdsCreate [options] instanceId classFQ dbName engine storage

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-d`         | Dry run - show command that would be executed                   |
| `-i integer` | IOPS; value must be at least 1000 if specified                  |
| `-P integer` | Port                                                            |
| `-p string`  | Master database user password, set to blahblah if not specified |
| `-q`         | Quiet mode; suppress all output                                 |
| `-r integer` | The number of days automated backups are retained               |
| `-u string`  | Master database user name, set to master if not specified       |
| `-w`         | Wait until operation has completed before exiting               |
| `-x`         | Debug mode                                                      |
| `-z string`  | [Availability Zone](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html); defaults to `us-east-1c` |

**Arguments**

| Argument     | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `instanceId` | Name of the new DB server                                                                                                            |
| `classFQ`    | One of: `micro`, `small`, `medium`, `large`, `xlarge`, `xxlarge`, `xxxlarge`, `4xlarge`, `8xlarge`                                   |
| `dbName`     | Name of the database to be managed by the new server                                                                                 |
| `engine`     | One of: `MySQL`, `postgres`, `oracle-se1`, `oracle-se`, `oracle-ee`, `sqlserver-ee`, `sqlserver-se`, `sqlserver-ex`, `sqlserver-web` |
| `storage`    | To be allocated, in GB                                                                                                               |


**Example**

Wait for a Postgres database server to be created on a micro instance in the default availability zone, default user id and password with ID `test`, a database called `testdb` and 10GB capacity.

    rdsCreate -w test micro testdb postgres 10

## rdsDelete
Deletes the specified database and all its snapshots, without making a final snapshot.
This operation takes several minutes, during which time rdsIds will continue to show that the database exists.

**Usage**

    rdsDelete [options] databaseId

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-h`         | Display help                                                    |
| `-w`         | Wait until operation has completed before exiting               |
| `-x`         | Debug mode                                                      |

**Example**

Wait for the Postgres database server with id `test` to be deleted.

    rdsDelete -w test

## rdsIds
Displays the `DBInstanceIdentifier` for each database owned by this account

**Usage**

    rdsIds [options]

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-d`         | Dry run                                                         |  
| `-h`         | Display help                                                    |  
| `-x`         | Debug mode                                                      |

## rdsStatus
Returns the run status of the RDS instance with the specified `instanceId`.
Values returned are: `available`, `backing-up`, `creating`, `deleting`, `failed`, `incompatible-network`, `incompatible-option-group`, `incompatible-parameters`, `incompatible-restore`, `modifying`, `rebooting`, `renaming`, `resetting-master-credentials` and `storage-full`.

**Usage**

    rdsStatus instanceId

**Example**

    rdsStatus `rdsIds`
