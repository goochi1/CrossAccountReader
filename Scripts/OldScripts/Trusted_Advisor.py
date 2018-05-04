import time
import pandas as pd
import xlsxwriter
import boto3


accounts="DevAccountNo.txt"

#https://pprakash.me/tech/2017/03/14/monitor-aws-trusted-advisor-checks/

textFile = open(accounts, "r").read()

# create an STS client object that represents a live connection to the
sts_client = boto3.client('sts')

#output types
security = []
cost_optimizing = []
fault_tolerance = []
performance = []

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
        'support',
        region_name='us-east-1',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken'],
    )

    # Use the Amazon IAM resource object that is now configured with the

    response = client.describe_trusted_advisor_checks(
    language='en'
        )
        
    
    for case in response["checks"]:
        cat = case["category"]
        
        if cat == "security":
           security.append(case["name"])
        if cat == "cost_optimizing":
           cost_optimizing.append(case["name"])
        if cat == "fault_tolerance":
           fault_tolerance.append(case["name"])
        if cat == "performance":
           performance.append(case["name"])

        s = pd.DataFrame({account_name : security})
        c = pd.DataFrame({account_name : cost_optimizing})
        f = pd.DataFrame({account_name : fault_tolerance})
        p = pd.DataFrame({account_name : performance})
        
    

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('Trust/%s.xlsx' %account_name, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        s.to_excel(writer, sheet_name='security')
        c.to_excel(writer, sheet_name='cost_optimizing')
        f.to_excel(writer, sheet_name='fault_tolerance')
        p.to_excel(writer, sheet_name='performance')

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

'''

    response = describe_trusted_advisor_check_result(
        checkId = 
    )
    # wait  

    #fileContent = response["Content"]
    # print fileContent
    
    for row in fileContent.split("\n"):
        username = row.split(",")[0]
        if username not in safeList:
            # prints out account number where the unknown user is
            outputcsv.write("%s,%s,%s\n" % (account_id, account_name, row))
'''
print 'done'
