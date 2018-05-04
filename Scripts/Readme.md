#Infrastucture
##Overview
keys can be found at vault read cloudops/passwords/AccountUser/AccountUser
Setup AccountUser and AccountUserProd using keys in vault


##Setup
You will need access keys from vault and set them as your default
aws configure --profile AccountUser

###Car.py
```
All functions shown below but in one script.
python car.py -env <Env> -f <Function>
List of accepted function parameters (eip, report, ec2_infomation, domain, update_trust_policy, add_account, list_accounts)
```

###AssumeRole
```
Basic Assume role that can be used with other boto scripts
http://boto3.readthedocs.io/en/latest/
python AssumeRole.py -env <Dev>
```
###Credential Report
```
Produces and excel sheet of all 'un-trusted' users that aren't in the safelist file.
this is used for auditing and to find unnecessary users in prod
(works in Dev and prod)
```
###Delete User
```
Removes user and all access from all accounts in list.
(only working in Dev)
```
###Update Trust Policy
```
Updates trust policy for new joiners.
Must update trusted relationship policy in policies
(works in Dev and prod)
python Update_Trust_Policy.py -env <Dev>
```
###Domain
```
Gets all hosted zones from all accounts and their sub domains with the records
(works in Dev and prod)
```

###EIP
```
Gets all EIPs associated to EC2s
(works in Dev and prod)
```
###Instance_IDs
```
Gets all EC2 instance IDs
(works in Dev and prod)
```

###Trusted_Advisor
```
Produces an excel file for each account with a list of things picked up on TA

Required: folder called 'Trust'
```

###CrossAccountInstanceCheck
```
Produces an excel file containing accounts with any ec2 instances
(Works in Dev and Prod)
python CrossAccountInstanceCheck.py -env <Dev>
```

###PrivilegedAccessReview
```
Produces an excel file containing list of users in each account and attached user and group policies
(Works in Dev and Prod)
python PrivilegedAccessReview.py -env <Dev>
```

###List_Accounts
```
Produces a csv containing all accounts in the organisation with Id and status
(List contains both Dev and Prod accounts)
```
