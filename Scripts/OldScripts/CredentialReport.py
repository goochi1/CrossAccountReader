import time

import boto3
accounts="DevAccountNo.txt"
# splits files into a list to be read in
safeList = open("safelist.txt", "r").read().strip("\n").split()

#accountList = open("AccountNo.txt", "r").read().strip("\n").split()

#Acc = [account("AAModellerUAT", "818446180355"), account("Sandbox","226342546049")]
textFile = open(accounts, "r").read()

# create an STS client object that represents a live connection to the
#if env == 'Dev':
session = boto3.Session(profile_name='AccountUser')
#else:
#session = boto3.Session(profile_name='AccountUserProd')
# Any clients created from this session will use credentials
# from the [dev] section of ~/.aws/credentials.
sts_client = session.client('sts')
#sts_client = boto3.client('sts')

# open file where report will go
outputcsv = open("output.csv", "w")

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.

for aws_account in textFile.split('\n'):
    #split text file
    account_name, account_id = aws_account.split(",")
    role_arn = "arn:aws:iam::%s:role/CrossAccountReader" % account_id
    print (account_name)
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

    response = client.generate_credential_report()
    # wait
    time.sleep(10)
    response = client.get_credential_report()
    fileContent = response["Content"]
    # print fileContent

    for row in fileContent.split(b"\n"):
        username = row.split(b",")[0]
        if username not in safeList:
            # prints out account number where the unknown user is
            outputcsv.write("%s,%s,%s\n" % (account_id, account_name, row))
outputcsv.close()

print ('done')
