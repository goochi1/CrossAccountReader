import boto3

policydocu="../Setup/readaccountsPolicy.json"
accounts="DevAccountNo.txt"

#open list of account no's
textFile = open(accounts, "r").read()
# create an STS client object that represents a live connection to the
policyDoc = open(policydocu, "r").read()
sts_client = boto3.client('sts')

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


    response = client.create_policy_version(
        PolicyArn="arn:aws:iam::%s:policy/ReadOnly" %account_id,
        PolicyDocument=policyDoc,
        SetAsDefault=True
    )


print ('done')
