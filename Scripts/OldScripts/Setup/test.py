
import os

textFile = open("AccountNo.txt", "r").read()
print "here"
print textFile
for aws_account in textFile.split('\n'):
    print aws_account
    profile, account_id = aws_account.split(",")
    command1="aws ec2 describe-instances --region us-west-1 --profile %s" %profile
    os.system (command1)
    print profile
print "done"
