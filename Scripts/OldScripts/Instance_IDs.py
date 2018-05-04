
import boto3
accounts="DevAccountNo.txt"

Instance_id = open("Instance_ID.csv", "w")

#splits files into a list to be read in
accountList = open(accounts,"r").read().strip("\n").split()
# create an STS client object that represents a live connection to the 
sts_client = boto3.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.

for aws_account in accountList:
    #split text file 
    account_name, account_id = aws_account.split(",")
    role_arn = "arn:aws:iam::%s:role/CrossAccountReader" % account_id
    print(role_arn)
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
        'ec2',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
	

    response = client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            # This will print will output the value of the Dictionary key 'InstanceId'
            #print(instance["InstanceId"])
            instid=(instance["InstanceId"])
            Instance_id.write("%s,%s,%s\n" % (account_id,account_name,instid))
	# Use the Amazon IAM resource object that is now configured with the 
	#you can now run commands useing the client that you have creted
	#e.g.
	#response = client.generate_credential_report()
	
Instance_id.close()
print ('done')
