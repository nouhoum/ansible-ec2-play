#!/usr/bin/env python

import subprocess
import sys
import simplejson as json

# Returns pending, running, stopping, stopped

if len(sys.argv)!=2:
  sys.exit('Usage: %s instanceId' % sys.argv[0])

instanceId = sys.argv[1]
p = subprocess.Popen("aws ec2 describe-instances --instance-ids {0}".format(instanceId), stdout=subprocess.PIPE, shell=True)
(output, err) = p.communicate()
#print output
reservations = json.loads(output)['Reservations']
for reservation in reservations:
  for instance in reservation['Instances']:
    print instance['State']['Name']
