#!/usr/bin/env python

import boto3
import sys

from dateutil import parser

region = sys.argv[1]

def newest_image(list_of_images):
    latest = None

    for image in list_of_images:
        if not latest:
            latest = image
            continue

        if parser.parse(image['CreationDate']) > parser.parse(latest['CreationDate']):
            latest = image

    return latest

client = boto3.client('ec2', region_name=region)

filters = [ {
        'Name': 'name',
        'Values': ['amzn-ami-hvm-*']
    },{
        'Name': 'description',
        'Values': ['Amazon Linux AMI*']
    },{
        'Name': 'architecture',
        'Values': ['x86_64']
    },{
        'Name': 'owner-alias',
        'Values': ['amazon']
    },{
        'Name': 'owner-id',
        'Values': ['137112412989']
    },{
        'Name': 'state',
        'Values': ['available']
    },{
        'Name': 'root-device-type',
        'Values': ['ebs']
    },{
        'Name': 'virtualization-type',
        'Values': ['hvm']
    },{
        'Name': 'hypervisor',
        'Values': ['xen']
    },{
        'Name': 'image-type',
        'Values': ['machine']
    } ]
 
response = client.describe_images(Owners=['amazon'], Filters=filters)
 
source_image = newest_image(response['Images'])
print(source_image['ImageId'])
