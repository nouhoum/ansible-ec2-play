# AWS RDS Support
These features require the [AWS RDS command-line toolkit](http://aws.amazon.com/developertools/2928). 
Documentation on the RDS command-line toolkit [here](http://docs.aws.amazon.com/AmazonRDS/latest/CommandLineReference/Welcome.html).

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
| `-r integer` | The number of days automated backups are retained               |
| `-u string`  | Master database user name, set to master if not specified       |
| `-q`         | Quiet mode; suppress all output                                 |
| `-x`         | Debug mode                                                      |
| `-z string`  | Availability Zone; examples: `us-east-1a`, `us-east-1b`, `us-west`, set to `us-east-1c` if not specified |

**Arguments**

| Argument     | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `instanceId` | is the name by which you wish to refer to the new DB server |
| `classFQ`    | is one of: `micro`, `small`, `medium`, `large`, `xlarge`, `xxlarge`, `xxxlarge`, `4xlarge`, `8xlarge` |
| `dbName`     | is the name of the database to be managed by the new server |
| `engine`     | is one of: `MySQL`, `postgres`, `oracle-se1`, `oracle-se`, `oracle-ee`, `sqlserver-ee`, `sqlserver-se`, `sqlserver-ex`, `sqlserver-web` |
| `storage`    | to be allocated, in GB |

## rdsDelete
Deletes the specified database and all its snapshots, without making a final snapshot.
This operation takes several minutes, during which time rdsIds will continue to show that the database exists.

**Usage**

    rdsDelete [options] databaseId

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| -x           | Debug mode                                                      |
| -h           | Display help                                                    |

## rdsIds
Displays the `DBInstanceIdentifier` for each database owned by this account

**Usage**

    rdsIds [options]

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| -h | Display help |  
| -x | Debug mode |
