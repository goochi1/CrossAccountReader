import boto3
import argparse
import subprocess

#setup parsar
parser = argparse.ArgumentParser(description='Update crossaccountaccess trust policy.')
parser.add_argument('-env', required=True, help='Enviroment Prod or Dev')
args = parser.parse_args()

#use as varibles
env = args.env

policydocu="Policies/%scrossTrustPolicy.txt" %env
accounts="%sAccountNo.txt" %env

#open list of account no's
textFile = open(accounts, "r").read()
# create an STS client object that represents a live connection to the
policyDoc = open(policydocu, "r").read()

if env == 'Dev':
    session = boto3.Session(profile_name='AccountUser')
else:
    session = boto3.Session(profile_name='AccountUserProd')
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.
sts_client = session.client('sts')

#sts_client = boto3.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.

error_list = []

for aws_account in textFile.split('\n'):
	try:

	    #split text file
	    account_name, account_id = aws_account.split(",")
	    role_arn = "arn:aws:iam::%s:role/CrossAccountReader" % account_id
	    print(account_name)
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

	    # Use the Amazon IAM resource object that is now configured with the
	    # Code for crediental report


	    response = client.update_assume_role_policy(
	        RoleName='CrossAccountAccess',
	        PolicyDocument=policyDoc

	    )
	except Exception as e:
		error_list.append(aws_account)
		print(e)


print('done')
if error_list:
	print("Please check the following accounts for errors (check for access denied)")
	print(error_list)
