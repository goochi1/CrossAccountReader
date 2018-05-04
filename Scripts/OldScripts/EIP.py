
import boto3
accounts="DevAccountNo.txt"

Instance_EIP = open("Instance_EIP.csv", "w")

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
        'ec2',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )
	

    response = client.describe_instances()
    #print response
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            for net in instance["NetworkInterfaces"]:
                
                if 'Association' in net:
                    ips = net["Association"]
                    #print ips
                    #print ips["PublicIp"]
                    item = ips["PublicIp"]
                        
                        #print net["Association"]
                       
                        #for j in i["PublicIp"]:
                                       
                    Instance_EIP.write("%s,%s,%s\n" % (account_id,account_name,item))
                else:
                    pass
	# Use the Amazon IAM resource object that is now configured with the 
	#you can now run commands useing the client that you have creted
	#e.g.
	#response = client.generate_credential_report()
	
Instance_EIP.close()
print 'done'
