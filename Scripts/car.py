import boto3
import argparse
import subprocess
import time
import os

 #setup parsar
def par():
    parser = argparse.ArgumentParser(description='Base for cross account reader.')
    parser.add_argument('-env', required=True, help='Enviroment Prod or Dev')
    parser.add_argument('-f', required=True, choices=['eip', 'report', 'ec2_infomation', 'domain', 'update_trust_policy','add_account', 'list_accounts'], help='which function do you want to use')
    args = parser.parse_args()

    #use as varibles
    global env
    global fun
    env = args.env
    fun = args.f
def assume(service):
    # Call the assume_role method of the STSConnection object and pass the role
    # ARN and a role session name.
    print (account_name)
    assumedRoleObject = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="AssumeRoleSession1"
    )
    credentials = assumedRoleObject['Credentials']
    global client
    client = boto3.client(
        service,
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

#read functions
def addaccount():
    #print ('\nAccount Name:'),
    AccountName = input("\nAccount Name: ")
    try:
        AccountNum = int(input("\nAccount Number: "))
    except ValueError:
        print ("\nPlease enter number:")

    accounts="%sAccountNo.txt" %env
    #file_path = "file.txt"
    par ()
    if os.path.exists(accounts):
        with open(accounts, 'a') as file:
            file.write("\n%s%s,%s" %(AccountName, env, AccountNum))  #adds account name, env and number to list

def eip():

    service = 'ec2'
    assume(service)
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

                    Output.write("%s,%s,%s\n" % (account_id,account_name,item))
def report():

    service = 'iam'
    assume(service)
    safeList = open("safelist.txt", "r").read().strip("\n").split()

    response = client.generate_credential_report()
    # wait  for report to generate
    time.sleep(10)
    response = client.get_credential_report()
    fileContent = response["Content"]
    # print fileContent

    for row in fileContent.split("\n"):
        username = row.split(",")[0]
        if username not in safeList:
            # prints out account number where the unknown user is
            Output.write("%s,%s,%s\n" % (account_id, account_name, row))
def ec2_infomation():

    service = 'ec2'
    assume(service)
    response = client.describe_instances()
    #print response
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instid=(instance["InstanceId"])
            #gets launch time
            lt=(instance["LaunchTime"])
            #gets AZ
            p = (instance["Placement"])
            az = (p["AvailabilityZone"])
            #gets ip
            for net in instance["NetworkInterfaces"]:

                if 'Association' in net:
                    ips = net["Association"]
                    #print ips
                    item = ips["PublicIp"]

                    Output.write("%s,%s,%s,%s,%s,%s\n" % (account_id,account_name,item,instid,az,lt))
def domain():

    service = 'route53'
    assume(service)
    response = client.list_hosted_zones()

    fileContent = response["HostedZones"]

    for zone in fileContent:
        zoneid = zone["Id"]
        #print zoneid
        responseRecord = client.list_resource_record_sets(
        HostedZoneId=zoneid
        )
        #print responseRecord

        for resourceSet in responseRecord["ResourceRecordSets"]:
            resourceName = resourceSet["Name"]
            #print resourceName
            #print resourceSet

            # if ResourceRecords is a Key
            if 'ResourceRecords' in resourceSet:
                for dns_record in resourceSet["ResourceRecords"]:
                    dns = dns_record['Value']

                    #print resourceName
                    #print dns
            elif 'AliasTarget' in resourceSet:
                alias = (resourceSet["AliasTarget"])
                dns = alias["DNSName"]

                #for dns_record in resourceSet["AliasTarget"]:
                    #dns = dns_record["DNSName"]
                    #print dns

                #pass
            else:
                print ("wtf")

                    #print out the record

            Output.write("%s,%s,%s,%s\n" % (account_id,account_name, resourceName, dns))
#write fucntions
def update_trust_policy():

    service = 'iam'
    assume(service)
    response = client.update_assume_role_policy(
        RoleName='CrossAccountAccess',
        PolicyDocument=policyDoc
    )

def list_accounts():
    
    client = session.client('organizations')
    paginator = client.get_paginator('list_accounts')
    print("Listing accounts...")
    # looping through the response iterator pages
    accounts = []
    for page in paginator.paginate():
        # Looping through the top level account and getting the account + status
        for account in page.get('Accounts'):
            row = [account.get('Id'), account.get('Name'), account.get('Status')]
            
            accounts.append(row)

    Output.write("Account ID,Account Name,Account Status\n")
    for row in accounts:
        Output.write('"%s","%s","%s"\n' % (row[0],row[1],row[2]))

def print_ascii():

    with open("ascii/asciiCar.txt") as f:
        f_ascii = f.read()
        print(f_ascii)

par()

policydocu="Policies/%scrossTrustPolicy.txt" %env
accounts="%sAccountNo.txt" %env
#open list of account no's
textFile = open(accounts, "r").read()
policyDoc = open(policydocu, "r").read()


with open("output.csv", "w") as Output:
# create an STS client object that represents a live connection to the
    if env == 'Dev':
        session = boto3.Session(profile_name='AccountUser')
    else:
        session = boto3.Session(profile_name='AccountUserProd')
        # Any clients created from this session will use credentials
        # from the [dev] section of ~/.aws/credentials.

    print_ascii()
    # List accounts doesn't need to assume role 
    if fun == 'list_accounts':
        list_accounts()
    else: 
        sts_client = session.client('sts')
        for aws_account in textFile.split('\n'):
        #split text file
            try:
                account_name, account_id = aws_account.split(",")
                role_arn = "arn:aws:iam::%s:role/CrossAccountReader" % account_id
                #print account_name

                if fun == 'eip':
                    eip()
                elif fun == 'report':
                    report()
                elif fun == 'ec2_infomation':
                        ec2_infomation()
                elif fun == 'domain':
                    domain()
                elif fun == 'update_trust_policy':
                    update_trust_policy()
                elif fun == 'add_account':
                    addaccount()
                    break
                else:
                    pass
            except Exception as e:
                print(e)


Output.close()
print ('Thank you for using CrossAccountReader')

