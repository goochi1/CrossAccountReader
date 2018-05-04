
import os

textFile = open("AccountNo.txt", "r").read()

for aws_account in textFile.split('\n'):
    #split text file 
	profile, account_id = aws_account.split(",")
	#Create Polciy
	command1="aws iam create-policy --policy-name ReadOnly --policy-document file://readaccountsPolicy.json --profile %s" %profile

	os.system (command1)

# Create Role
	command2= "aws iam create-role --role-name CrossAccountReader --assume-role-policy-document file://CCATrustPolicy.json --profile %s" %profile
	os.system (command2)

# Attach readonly Policy
	command3= "aws iam attach-role-policy --policy-arn arn:aws:iam::%s:policy/ReadOnly --role-name CrossAccountReader --profile %s" %(account_id, profile)
	os.system (command3)
	print profile

print "done"
