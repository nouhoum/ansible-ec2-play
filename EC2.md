# EC2 Utilities

## ec2Ids
Displays all EC2 instance ids for this AWS account.

**Usage** 

    ec2Ids [options]

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| -h           | Display help                                                    |
| -x           | Debug mode                                                      |

## ec2Info
Given an EC2 instance id, return the IP address, domain name or status

**Usage**

    ec2Info [option] i-7cf09e18

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| -h           | Display help                                                    |
| -i           | return IP address (no output if the instance is stopped)        |
| -n           | return DNS name (no output if the instance is stopped)          |
| -s           | return status (running or stopped)                              |
| -x           | Debug mode                                                      |

## ec2InstanceId 
Given an EC2 domain name or IP address, returns the EC2 instance id.
Domain name must be of the form: ec2-54-196-57-227.compute-1.amazonaws.com

**Usage**

    ec2InstanceId [options] id

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| -h           | Display help                                                    |
| -i           | return IP address                                               |
| -n           | return DNS name                                                 |
| -x           | Debug mode                                                      |

**Examples**

````
ec2InstanceId i-7cf09e18
aws ec2 stop-instances --instance-ids 
aws ec2 start-instances --instance-ids 
````

## ec2Start
Starts the EC2 instance with the specified instanceId.

**Usage**

    ec2Start [options] instanceId

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| -h           | Display help                                                    |
| -x           | Debug mode                                                      |

## ec2Stop
Stops the EC2 instance with the specified instanceId.

**Usage**

    ec2Stop [options] instanceId

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| -h           | Display help                                                    |
| -x           | Debug mode                                                      |
