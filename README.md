# Ansible EC2 Play Framework
This is a set of Ansible scripts to deploy Play 2.2+ web applications in EC2 instances.
Play applications are run as a system service.
Play 2.2 uses SBT 0.13, and has a different deploy directory, which is handled in this version.
The EC2 instances should be 'small' or larger; 'micro' instances won't compile.

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

* `bootstrap`: secures an EC2 Ubuntu AMI. Requires `sudo`.
* `playenv`: sets play dependencies (pvm, java). Requires `sudo`.
* `service`: defines system service for play application. Requires `sudo`.
* `deploy`: clones a Play project from a Git repository and deploys it on the machine. `sudo` is not required.
* `launch`: Launches the deployed app, killing it first if necessary. `sudo` is not required.

Run individual Ansible scripts this way:

    bin/run script_name [sudo]

You can also run all of the scripts in order this way:

    bin/runAll

## Utility Scripts
The `bin` directory contains [EC2](EC2.md) and [RDS](RDS.md) utility scripts.

## System Service
If you are logged into the remote server, you can start, restart and stop the Play application system service like this:

    sudo service play start
    sudo service play restart
    sudo service play stop


## References
* [The original source which inspired most of these scripts](https://github.com/phred/5minbootstrap)
* [My first 5 minutes on a server](http://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers)
* [A blog post that the author of the preceding article wrote](http://practicalops.com/my-first-5-minutes-on-a-server.html)
