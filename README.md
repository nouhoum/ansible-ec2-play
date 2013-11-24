# Ansible EC2 Play Framework
This is a set of Ansible scripts to deploy Play 2 projects in EC2 instances.
The EC2 instances should be 'small' or larger; 'micro' instances won't compile.

**WARNING: USE AT YOUR OWN RISK. NO WARRANTY, EXPRESS OR IMPLIED IS PROVIDED. ASSUME THIS PROJECT WAS CREATED BY FOOLS!**

Steps to use:

* edit `hosts.ini` and set your ec2 instance name(s)
* edit `yaml/config/postfix_selections` to set domains for email 
* Add the Amazon AWS keys for your EC2 instances to your local `ssh` repository by running the following:
```` 
    ssh-agent && ssh-add ~/path/to/foo.pem
````

## Scripts
Scripts may contain variables that need to be customized for your specific deployments. 
Commonly modified variables have been factored into `bin/custom.sample`. 
Make a copy of that file and save as `bin/custom` before modifying.

    cp bin/custom{.sample,}

The following scripts are available in the `yaml` directory:

* `bootstrap`: secures an EC2 Ubuntu AMI. Requires `sudo`.
* `playenv`: sets play dependencies (pvm, java) including Authbind so Play can use port 80 without root privileges. Requires `sudo`.
* `deploy`: clones a Play project from a Git repository and deploys it on the machine. `sudo` is not required.

* Run individual Ansible scripts this way:
````
    bin/run script_name [sudo]
````
* You can also run all of the scripts this way:
````
    bin/runAll
````

## Start file
The settings assume the use of [Authbind](http://en.wikipedia.org/wiki/Authbind) so Play can run on port 80 without root privileges. 
A `start` file is provided in the `exec` directory which can be used as a template for your own `start` file.

Deployment scripts assume you check in your customized `start` file at the root of the git project. Modify the script accordingly if that is not the case.

## Sources
* [The original source which inspired most of these scripts](https://github.com/phred/5minbootstrap)
* A blog post that the author of 5minbootstrap wrote. [Check it out! ](http://practicalops.com/my-first-5-minutes-on-a-server.html)
* [This excellent post](http://plusbryan.com/my-first-5-minutes-on-a-server-or-essential-security-for-linux-servers)


