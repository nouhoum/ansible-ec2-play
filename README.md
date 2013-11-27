# Ansible EC2 Play Framework
This is a set of Ansible scripts to deploy Play 2.2+ web applications and Postgres database in EC2 instances.
The EC2 instances for Play should be 'small' or larger; 'micro' instances won't be able to compile the Play app.
Play applications are run as a system service.

This project uses EC2 instance IDs to reference EC2 instances, because their IP addresses and DNS names change on every restart unless you have provisioned permanent IP addresses.

**WARNING: USE AT YOUR OWN RISK. NO WARRANTY, EXPRESS OR IMPLIED IS PROVIDED.**

## Steps

1. If your git repository is private and therefore requires authentication:

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
5. Edit `hostIds` and enter your ec2 instance id(s), one per line. Keep this file up to date as you add and remove EC2 instances.
6. Run `bin/makeHostIni` to create or update `hosts.ini`. Do this every time you add an ec2 instance id to `hostIds`. 
   You also need to do this each time an AWS EC2 instance is restarted unless you have provisioned permanent IP addresses.

## Ansible Scripts
Scripts may contain variables that need to be customized for your specific deployments. 
Commonly modified variables have been factored into `bin/custom.sample`. 
Make a copy of that file and save as `bin/custom` before modifying.

    cp bin/custom{.sample,}

The following scripts are available in the `yaml` directory:

| Name          | Description                                                                                                             |
| ------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `bootstrap`   | Sets up an EC2 Ubuntu AMI.                                                                                              |
| `playEnv`     | Installs Play dependencies such as `pvm` and `java`.                                                                    |
| `playService` | Defines a system service for the Play application.                                                                      |
| `playDeploy`  | Clones a Play project from a Git repository and deploys it on the machine.                                              |
| `playLaunch`  | Launches the deployed Play app, killing the previous instance first if necessary.                                       |
| `postgresEnv` | Installs Postgres dependencies such as `pvm` and `java`. Use `psql` to restore the database before running `playLaunch` |

Run individual Ansible scripts on the hosts with IDs listed in `hostIds` like this (`-s` causes the script to run as superuser via `sudo`):

    bin/run scriptName

**Usage**

    bin/run [options] script

Where `script` is one of the above Ansible scripts.

**Options**

| Option       | Description                                                     |
| ------------ | --------------------------------------------------------------- |
| `-d`         | Dry run, shows commands that would be executed                  |
| `-h`         | Display help                                                    |
| `-j`         | Selects the host.ini section, defaults to ec2Instances          |
| `-v`         | increments verbose output (can be specified up to 3 times)      |
| `-x`         | Debug mode                                                      |

### provisionPlay
The `provisionPlay` script runs all of the Ansible scripts necessary to provision Play on the EC2 instances with IDs listed in the `playServers` section in `hosts.ini`.
Options are the same as for the `run` script above.

### provisionPostgres
The `provisionPostgres` script runs all of the Ansible scripts necessary to provision Postgres on the EC2 instances with IDs listed in the 'postgresServers' section in `hosts.ini`.
Options are the same as for the `run` script above.

## Utility Scripts
The `bin` directory contains [EC2](EC2.md) and [RDS](RDS.md) utility scripts.

## System Service
If you are logged into the remote server, you can start, restart and stop the Play application system service like this:

    sudo service play start
    sudo service play restart
    sudo service play stop

## Sample Session
Database servers should be provisioned before the application servers.

    # Create a Ubuntu 13.10 micro image in the default availability zone with the default security group. 
    # Define key pair scalaCourses if it does not already exist.
    ec2Create scalaCoursesDB scalaCourses t1.micro ami-51274050
    provisionPostgres

    # Create a Ubuntu 13.10 micro image in the default availability zone with the default security group. 
    # Use the scalaCourses key pair.
    ec2Create scalaCoursesPlay scalaCourses t1.micro ami-51274050
    provisionPlay

## References
* [The original source which inspired most of these scripts](https://github.com/phred/5minbootstrap)
* [My first 5 minutes on a server](http://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers)
* [A blog post that the author of the preceding article wrote](http://practicalops.com/my-first-5-minutes-on-a-server.html)
