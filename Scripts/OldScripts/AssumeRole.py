import boto3
import argparse
import subprocess

#setup parsar
parser = argparse.ArgumentParser(description='Base for cross account reader.')
parser.add_argument('-env', required=True, help='Enviroment Prod or Dev')
args = parser.parse_args()

#use as varibles
env = args.env

accounts="%sAccountNo.txt" %env

#open list of account no's
textFile = open(accounts, "r").read()
# create an STS client object that represents a live connection to the
if env == 'Dev':
    session = boto3.Session(profile_name='AccountUser')
else: 
    session = boto3.Session(profile_name='AccountUserProd')
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.
sts_client = session.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.

for aws_account in textFile.split('\n'):
    #split text file 
    account_name, account_id = aws_account.split(",")
    role_arn = "arn:aws:iam::%s:role/CrossAccountReader" % account_id
    print account_name
    assumedRoleObject = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AssumeRoleSession1"
    )

    # From the response that contains the assumed role, get the temporary
    # credentials that can be used to make subsequent API calls
    credentials = assumedRoleObject['Credentials']

    # Use the temporary credentials that AssumeRole returns to make a
    # connection to Amazon IAM
    client = boto3.client(
        'iam',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

	##########CODE########

print 'done'