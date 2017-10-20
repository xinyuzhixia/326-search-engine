import boto3

def main()

	ec2 = boto3.client('ec2', 
		# hard code the user's credentials
		aws_access_key_id = 'AKIAIHBI3K2OP5ZMCWEA'
		aws_secret_access_key = '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'
		region_name = 'us-east-1'
		)

	response = ec2.create_key_pair(KeyName='KEY_PAIR_NAME')
	print (response)

	return

if __name__ == "__main__":
    main()