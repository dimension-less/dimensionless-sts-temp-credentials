import os
import sys
import boto3
import json
import requests
import argparse
import ConfigParser
from botocore.exceptions import ClientError


def get_credentials():
    client = boto3.client('sts')
    assumed_role_object = client.assume_role(
        RoleArn="arn:aws:iam::701297840991:role/admin",
        RoleSessionName="AssumeRoleSession1"
    )
    print(assumed_role_object['Credentials']['SecretAccessKey'])
    print(assumed_role_object['Credentials']['AccessKeyId'])
    return assumed_role_object['Credentials']


def write_credentials(profile, credentials):
    filename = os.path.expanduser('~/.aws/credentials')
    dirname = os.path.dirname(filename)

    if not os.path.exists(dirname):
        os.makedirs(dirname)

    config = ConfigParser.ConfigParser()
    config.read(filename)
    if not config.has_section(profile):
        config.add_section(profile)
    config.set(profile, 'aws_access_key_id', credentials['AccessKeyId'])
    config.set(profile, 'aws_secret_access_key', credentials['SecretAccessKey'])
    config.set(profile, 'aws_session_token', credentials['SessionToken'])
    with open(filename, 'w') as fp:
        config.write(fp)


if __name__ == '__main__':
    credential = get_credentials()
    write_credentials('default', credential)
