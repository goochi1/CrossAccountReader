import boto3

print '\nWhat User do you want to remove?',
user_name = raw_input()

print '\nAre you sure you want remove %s?\n Type yes or no:' % user_name,
check = raw_input()

if check == 'yes':
    #open list of account no's
    accounts="DevAccountNo.txt"
    textFile = open(accounts, "r").read()
    #user_name = 'user'
    # create an STS client object that represents a live connection to the
    sts_client = boto3.client('sts')


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

        # Use the Amazon IAM resource object that is now configured with the
        # Code for crediental report
        try:
            #Detach POLICES
            #get policies attached to the user
            response = client.list_attached_user_policies(UserName=user_name)
            #for each item in the attached polies dictonary select polname from the list[] add to polNames list
            for x in response["AttachedPolicies"]:
                response = client.detach_user_policy(
                    UserName=user_name,
                    PolicyArn=x["PolicyArn"]
                )
            print "Removed Policy ", y['PolicyArn']

            #DETACH GROUPS
            response = client.list_groups_for_user(UserName=user_name)
            #for each item in the attached polies dictonary select polname from the list[] add to polNames list
            for y in response["Groups"]:
                response = client.remove_user_from_group(
                    UserName=user_name,
                    GroupName=y["GroupName"]
                )
            print "Removed Group ", y['GroupName']


            #Delete ACCESS KEYS
            response = client.list_access_keys(UserName=user_name)
            for z in response["AccessKeyMetadata"]:
                response = client.delete_access_key(
                    UserName=user_name,
                    AccessKeyId=z["AccessKeyId"]
                )
            print 'removed_accesskeys'

            #DELTE LOGIN PROFILE
            try:
                response = client.delete_login_profile(UserName=user_name)
                print 'delete_profile'
            except:
                print "no profile so error'd"
            
            #DELETE USER
            response = client.delete_user(UserName=user_name)
            print "removed user: ", user_name
        
        except:
            print "no user"

else:
    pass


print 'done'
