# Ansible EC2 Play Framework
This is a set of Ansible scripts to deploy Play 2.2+ web applications in EC2 instances.
The EC2 instances for Play should be 'small' or larger; 'micro' instances won't be able to compile the Play app.
Play applications are run as a system service.
This project uses EC2 instance IDs to reference EC2 instances, because their IP addresses and DNS names change on every restart unless you have provisioned permanent IP addresses.

An Ansible script is provided to setup a Postgres database in an EC2 instance.
Support for AWS RDS Postgres is also provided via the `bin/rds*` commands.

**WARNING: USE AT YOUR OWN RISK. NO WARRANTY, EXPRESS OR IMPLIED IS PROVIDED.**

## Dependencies

Install and configure the following.

* [Ansible](https://github.com/ansible/ansible)
* [jq](http://stedolan.github.io/jq/download/), a lightweight and flexible command-line JSON processor.
* [AWS command-line toolkit](http://aws.amazon.com/developertools/2928). 
[General AWS command-line documentation](http://aws.amazon.com/cli/).
[AWS RDS command-line documentation](http://docs.aws.amazon.com/AmazonRDS/latest/CommandLineReference/Welcome.html).

## Steps

1. If the git repository that holds your Play project is private and therefore requires authentication:

  a. Run the following on every EC2 instance as root (not sure how to automate this)
    
    i. GitHub
````
ssh-keyscan github.com >> /etc/ssh/ssh_known_hosts
````

     ii. BitBucket
````
ssh-keyscan bitbucket.org >> /etc/ssh/ssh_known_hosts
````
    b. Add the public key for your EC2 instances to the owner's account of the github or bitbucket repository
2. Edit `/etc/ansible/ansible.cfg` and change this:
````
transport=paramiko
````
to this:
````
transport=ssh
````
3. Edit `yaml/config/postfix_selections` to set domains for email 
4. Add the Amazon AWS keys for your EC2 instances to your local `ssh` repository by running the following:
```` 
    ssh-agent && ssh-add ~/path/to/foo.pem
````
6. Run `bin/hostIni` to create or update `hosts.ini`.  
   You also need to do this each time an AWS EC2 instance is restarted unless you have provisioned permanent IP addresses.
5. Edit `hostIds` and enter the instance id(s) of pre-existing EC2 instances, one per line. 
   This file is automatically kept up to date by the `bin/` scripts as you add and remove EC2 and RDS instances.

## Bash Scripts
The `bin` directory contains bash scripts for [EC2](EC2.md) and [RDS](RDS.md) operation, and also contains undocumented utility bash scripts.

## Ansible Scripts
Scripts may contain variables that need to be customized for your specific deployments. 
Commonly modified variables have been factored into `bin/custom.sample`. 
Make a copy of that file and save as `bin/custom` before modifying.

    cp bin/custom{.sample,}

The following Ansible scripts are available in the `yaml` directory:

| Name          | Description                                                                                                             |
| ------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `bootstrap`   | Sets up an EC2 Ubuntu AMI.                                                                                              |
| `playEnv`     | Installs Play dependencies such as `pvm` and `java`.                                                                    |
| `playService` | Defines a system service for the Play application.                                                                      |
| `playDeploy`  | Clones a Play project from a Git repository and deploys it on the machine.                                              |
| `playLaunch`  | Launches the deployed Play app, killing the previous instance first if necessary.                                       |
| `postgresEnv` | Installs Postgres on a generic AWS EC2 instance, as an alternative to using an AWS RDS Postgres instance such as those created by `bin/rdsCreate`. Use `bin/psql` to restore the database before running `playLaunch` |

**Usage**

Run individual Ansible scripts on the hosts with IDs listed in `hosts.ini` like this:

    bin/run [options] scriptName

Where `scriptName` is one of the above Ansible scripts.

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-d`         | Dry run, shows commands that would be executed                  |
| `-h`         | Display help                                                    |
| `-v`         | increments verbose output (can be specified up to 3 times)      |
| `-x`         | Debug mode                                                      |

### hosts.ini
This file drives the Ansible scripts.
It is automatically maintained through the bash scripts in the `bin/` directory.
This file contains 6 sections: 

1. A section listing the EC2 instanceIDs of generic EC2 servers: `ec2Instances.ids` 
2. A section listing the EC2 instanceIDs of Play servers: `playServers.ids`
3. A section listing the EC2 instanceIDs of Postgres servers: `postgresServers.ids`
4. A section listing the EC2 domain names of generic EC2 servers: `ec2Instance.domains` 
5. A section listing the EC2 domain names of Play servers: `playServers.domains`
6. A section listing the EC2 domain names of Postgres servers: `postgresServers.domains`

Note that each entry in the `playServer.ids` and `postgresServer.ids` sections should also appear in the `ec2Instance.ids` section.
Similarly, each entry in the `playServer.domains` and `postgresServer.domains` sections should also appear in the `ec2Instance.domains` section.

The `bin/hostIni` command updates the three `*.domain` sections from the corresponding `*.ids` sections, removes dead entries, and is automatically invoked by the `bin/` scripts when adding and deleting servers.

````
[ec2Instances.ids]
i-8ae6adf1
i-06c83262
i-9cd52ff8
i-f0560794
i-12136369

[playServers.ids]
i-f0560794
i-12136369

[postgresServers.ids]
i-8ae6adf1

[ec2Instance.domains]

[playServers.domains]

[postgresServers.domains]
````

### provisionPlay
The `bin/provisionPlay` script runs all of the Ansible scripts necessary to provision Play on the EC2 instances with IDs listed in the `playServers` section in `hosts.ini`.
Options are the same as for the `run` script above.

### provisionPostgres
The `bin/provisionPostgres` script runs all of the Ansible scripts necessary to provision Postgres on the EC2 instances with IDs listed in the `postgresServers` section in `hosts.ini`.
Options are the same as for the `run` script above.

## System Service
If you are logged into the remote server, you can start, restart and stop the Play application system service like this:

    sudo service play start
    sudo service play restart
    sudo service play stop

## Sample Session
Database servers should be provisioned before the application servers.

    # Create an Ubuntu 13.10 micro instance in the default availability zone with the default security group.
    # Define key pair scalaCourses if it does not already exist.
    bin/ec2Create scalaCoursesDB scalaCourses t1.micro ami-4b143122 postgresServers 
    bin/provisionPostgres

    # Create an Ubuntu 13.10 micro instance in the default availability zone with the default security group.
    # Use the scalaCourses key pair again.
    bin/ec2Create scalaCoursesPlay scalaCourses t1.micro ami-4b143122 playServers
    bin/provisionPlay

## References
* [The original source which inspired most of these scripts](https://github.com/phred/5minbootstrap)
* [My first 5 minutes on a server](http://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers)
* [A blog post that the author of the preceding article wrote](http://practicalops.com/my-first-5-minutes-on-a-server.html)

## Sponsor
This project is sponsored by [Micronautics Research](http://micronauticsresearch.com),
developer of [ScalaCourses.com](http://scalacourses.com)
