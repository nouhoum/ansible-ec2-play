# Ansible EC2 Play Framework
This is a set of Ansible scripts to deploy Play 2.2+ web applications in EC2 instances.
The EC2 instances for Play should be 'small' or larger; 'micro' instances are not able to compile Play applications.
Play applications are run as a system service.
This project uses EC2 instance IDs to reference EC2 instances, because their IP addresses and DNS names change on every restart unless you have provisioned permanent IP addresses.

[An Ansible script](yaml/postgresEnv.yaml) is provided to setup a Postgres database in an EC2 instance.
Support for AWS RDS Postgres is also provided via the [`bin/rds*`](bin) commands.

[Dependencies](#dependencies) must be installed and [Setup](#setup) must be performed before this project's scripts will work.


**WARNING: USE AT YOUR OWN RISK. NO WARRANTY, EXPRESS OR IMPLIED IS PROVIDED.**

## Bash Scripts
The `bin` directory contains bash scripts for EC2 and RDS operation, and also contains utility bash scripts.
End user bash scripts are described in the [EC2 bash script documentation page](EC2.md), the [RDS bash script documentation page](RDS.md) and in this section.
Internal bash scripts invoked by the above are documented [here](INTERNAL.md#bash-scripts).
Ansible scripts invoked by the bash scripts are documented [here](INTERNAL.md#ansible-scripts).

### provisionPlay
The `bin/provisionPlay` script runs the necessary Ansible scripts to provision Play on the EC2 instances with IDs listed in the `playServers` section in [`hosts.ini`](#hostsini).
Options are the same as for the [`run` script](BASH.md#run).

### provisionPostgres
The `bin/provisionPostgres` script runs the necessary Ansible scripts to provision Postgres on the EC2 instances with IDs listed in the `postgresServers` section in `hosts.ini`.
Options are the same as for the [`run` script](BASH.md#run).

## Play System Service
If you are logged into an EC2 server that has been provisioned as a Play server, you can start, restart and stop the Play application system service like this:

    sudo service play start
    sudo service play restart
    sudo service play stop

## Sample Session
Database servers should be provisioned before the application servers.
You can either use the [`bin/rdsCreate`](RDS.md#rdscreate) command to create an AWS RDS database, or do the following to create a Postgres database using an Ansible script.

    # Create an Ubuntu 13.10 micro instance in the default availability zone with the default security group.
    # Define key pair scalaCourses if it does not already exist.
    # Wait for the command to complete before returning.
    bin/ec2Create -w scalaCoursesDB scalaCourses t1.micro ami-4b143122 postgresServers
    bin/provisionPostgres

Regardless of how you provisioned your database, your next step is to provision a Play 2 server:

    # Create an Ubuntu 13.10 micro instance in the default availability zone with the default security group.
    # Use the scalaCourses key pair again.
    # Wait for the command to complete before returning.
    bin/ec2Create -w scalaCoursesPlay scalaCourses t1.micro ami-4b143122 playServers
    bin/provisionPlay

Each time you run `provisionPostgres` or `provisionPlay` all of the servers mentioned in `hosts.ini` are reprovisioned.
Provisioning only needs to be done once, so the `ec2Create` bash script causes the contents of `hosts.ini` to be replaced by new server's domain name in the appropriate sections of that file.

## Dependencies

Install and configure the following.

* [Ansible](https://github.com/ansible/ansible)
* [jq](http://stedolan.github.io/jq/download/), a lightweight and flexible command-line JSON processor.
* [AWS command-line toolkit](http://aws.amazon.com/developertools/2928).
[General AWS command-line documentation](http://aws.amazon.com/cli/).
[AWS RDS command-line documentation](http://docs.aws.amazon.com/AmazonRDS/latest/CommandLineReference/Welcome.html).

## Setup

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
3. Edit [`yaml/config/postfix_selections`](yaml/config/postfix_selections) to set up   email.
4. Persistent data about the servers, including sensitive information, is stored in JSON format.
   Set the `ANSIBLE_DATA_DIR` environment variable to define the location of the directory to read/write your data from/to.
   If the variable is not set, a directory called `data` will be created for this purpose within this project.
   Beware: this information contains passwords and ssh keys.
   Take steps to secure it!
5. Copy the Amazon AWS keys for your existing EC2 instances to the `$ANSIBLE_DATA_DIR` directory.
6. Add the Amazon AWS keys for your existing EC2 instances that won't be ignored by this project to your local `ssh` repository by running the following:
````
    ssh-agent && ssh-add $ANSIBLE_DATA_DIR/foo.pem
````

## References
* [The original source which inspired most of these Ansible scripts](https://github.com/phred/5minbootstrap)
* [My first 5 minutes on a server](http://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers)
* [A blog post that the author of the preceding article wrote](http://practicalops.com/my-first-5-minutes-on-a-server.html)

## Sponsor
This project is sponsored by [Micronautics Research](http://micronauticsresearch.com),
developer of [ScalaCourses.com](http://scalacourses.com)
