#!/usr/bin/env python

import rospkg
import sys
import yaml

user_modules = sys.argv[1:]

# Get param file path from ROS package
rospack = rospkg.RosPack()
try:
    param_file = rospack.get_path('asv_description') + '/param/vehicle.yaml'
except rospkg.ResourceNotFound as exp:
    print "update_modules.py: %s package not found" % exp 
    sys.exit(1)

# Load param file as yaml
with open(param_file) as f:
    yaml_file = yaml.load(f)

# Update modules field
yaml_file['modules'] = []
for mod in user_modules:
    yaml_file['modules'].append('%s' % mod)

# Check if modules list is empty
if not yaml_file['modules']:
    yaml_file['modules'].append('')

# Save modified yaml file
with open(param_file, 'w') as f:
    yaml.dump(yaml_file, f)

sys.exit(0)