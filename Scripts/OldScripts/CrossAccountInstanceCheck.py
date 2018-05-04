import boto3
import argparse
import subprocess
import csv
from botocore.exceptions import ClientError

#setup parsar
parser = argparse.ArgumentParser(description='Check Accounts for EC2 Instances')
parser.add_argument('-env', required=True, help='Enviroment Prod or Dev')
args = parser.parse_args()

#use as varibles
env = args.env
instancerunning = "%s_contains_instances.csv" %env
instance_running = open(instancerunning, "w", newline='')
writer = csv.writer(instance_running)
writer.writerow(["Account Name", "Account ID"])

accounts="%sAccountNo.txt" %env
#splits files into a list to be read in
accountList = open(accounts,"r").read().strip("\n").split()
# create an STS client object that represents a live connection to the
if env == 'Dev':
    session = boto3.Session(profile_name='AccountUser')
else:
    session = boto3.Session(profile_name='AccountUserProd')
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.
sts_client = session.client('sts')


for aws_account in accountList:
    #split text file
    account_name, account_id = aws_account.split(",")
    role_arn = "arn:aws:iam::%s:role/CrossAccountReader" % account_id
    print (account_name)
    try:
        assumedRoleObject = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName="AssumeRoleSession1"
        )
    except ClientError as e:
        print("NA")
        continue



    # From the response that contains the assumed role, get the temporary
    # credentials that can be used to make subsequent API calls
    credentials = assumedRoleObject['Credentials']

    # Use the temporary credentials that AssumeRole returns to make a
    # connection to Amazon IAM
    client = boto3.client(
        'ec2',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
    # Get info on instances from current role and print to csv
    instances = client.describe_instances()
    instances = instances['Reservations']
    if len(instances) > 0:
      print('Contains Instances')
      row = [account_name,account_id]
      writer.writerow(row)


instance_running.close()
print("done")
