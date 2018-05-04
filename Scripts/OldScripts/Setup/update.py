
import os

textFile = open("AccountNoProd.txt", "r").read()

for aws_account in textFile.split('\n'):
    #split text file 
    profile, account_id = aws_account.split(",")
    print profile
    #update Polciy
    command1 = "aws iam create-policy-version --policy-arn arn:aws:iam::%s:policy/ReadOnly --policy-document file://readaccountsPolicyProd.json --set-as-default --profile %s" %(account_id, profile)
    os.system (command1)
