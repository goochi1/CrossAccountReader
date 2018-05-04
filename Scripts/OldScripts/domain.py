
import boto3
import argparse

parser = argparse.ArgumentParser(description='Process inputs for ssl.')
parser.add_argument('-env', help='enviroment var')
args = parser.parse_args()

env = args.env
args = vars(parser.parse_args())

if not any(args.values()):
    parser.error('No arguments provided.')

accounts="%sAccountNo.txt" %env

domaintxt = open("domain.csv", "w")

#splits files into a list to be read in
accountList = open(accounts,"r").read().strip("\n").split()
# create an STS client object that represents a live connection to the 
sts_client = boto3.client('sts')

# Call the assume_role method of the STSConnection object and pass the role
# ARN and a role session name.

for aws_account in accountList:
	#used %s for varible
	account_name, account_id = aws_account.split(",")
	role_arn = "arn:aws:iam::%s:role/CrossAccountReader"%account_id
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
	    'route53',
	    aws_access_key_id = credentials['AccessKeyId'],
	    aws_secret_access_key = credentials['SecretAccessKey'],
	    aws_session_token = credentials['SessionToken']
	)
	

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
				print "wtf"

					#print out the record 
				
			domaintxt.write("%s,%s,%s,%s\n" % (account_id,account_name, resourceName, dns))
				
	# Use the Amazon IAM resource object that is now configured with the 
	#you can now run commands useing the client that you have creted
	#e.g.
	#response = client.generate_credential_report()
	

domaintxt.close()
print 'done'

'''
def test
  expected = [{}]
  result = get_dns_record(resourceSet["ResourceRecords"])
  assert expected, result



def get_dns_record(resourceRecords):
	return [dns_record for dns_record in resourceRecords['ResourceRecords']]
'''