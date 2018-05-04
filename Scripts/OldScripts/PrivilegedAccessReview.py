import time
from botocore.exceptions import ClientError
import boto3
import argparse
import csv

#setup parser
parser = argparse.ArgumentParser(description='Check prod or dev accounts')
parser.add_argument('-env', required=True, help='Prod or Dev')
args = parser.parse_args()

env = args.env

if env == 'Dev':
    session = boto3.Session(profile_name='AccountUser')
    accounts="DevAccountNo.txt"
else:
    session = boto3.Session(profile_name='AccountUserProd')
    accounts="ProdAccountNo.txt"

# splits files into a list to be read in
safeList = open("safelist.txt", "r").read().strip("\n").split()

#accountList = open("AccountNo.txt", "r").read().strip("\n").split()

#Acc = [account("AAModellerUAT", "818446180355"), account("Sandbox","226342546049")]
textFile = open(accounts, "r").read()

# create an STS client object that represents a live connection to the
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.
sts_client = session.client('sts')
#sts_client = boto3.client('sts')

# open file where report will go
outputcsv = open("PrivilegedAccessReview.csv", "w", newline='')
writer = csv.writer(outputcsv)
writer.writerow(["Account Name", "Account ID", "Username", "User Policies", "Group Policies"])

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.

for aws_account in textFile.split('\n'):
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
        'iam',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],

    )
###############################################################################
# Get list of users in acccount
    dict_users = client.list_users()
    dict_users = dict_users['Users']
    users = []
    for user in dict_users:
        users.append(user['UserName'])
    #print(users)

##############################################################################
# Loop through users

    for user_name in users:
        print(user_name)

##############################################################################
# Get in-line user policies?

        inline_user_policies = client.list_user_policies(UserName = user_name)
        fileContent1 = inline_user_policies['PolicyNames']
        #print(fileContent1)

        # Use the Amazon IAM resource object that is now configured with the
        # Code for privileged access review
    ###############################################################################
    #Get list of attached user policies
        response = client.list_attached_user_policies(
        UserName=user_name,
        )
        fileContent = response['AttachedPolicies']
        attached_policies = []
        for policy in fileContent:
            attached_policies.append(policy['PolicyName'])
        attached_policies = str(attached_policies).strip('[' + ']')
        #print(attached_policies)
    #############################################################################
    #Get list of attached groups
        response = client.list_groups_for_user(UserName = user_name)
        response = response['Groups']
        #print(response)
        groups = []
        for dict in response:
            #print(dict)
            groups.append(dict["GroupName"])
        #print(groups)
    #############################################################################
    #Get lists of attached group policies for each group
        group_policies = []
        for group in groups:
               response = client.list_attached_group_policies(GroupName=group)
               response = response['AttachedPolicies']
               for policy in response:
                   group_policies.append(policy['PolicyName'])
        group_policies = str(group_policies).strip('[' + ']')
        #group_policies = group_policies.strip('[' + ']')
        #print(group_policies)
        #row = [account_name, account_id, user_name, attached_policies, group_policies]
        # wait

        writer.writerow([account_name, account_id, user_name, attached_policies, group_policies])

outputcsv.close()
print ('done')
