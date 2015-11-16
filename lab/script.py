import boto.ec2

f = open('credentials.csv','r')
line = f.readline()
parsed_line = line.split(',')
aws_access_key_id = parsed_line[3].strip()
aws_secret_access_key = parsed_line[4].strip()

conn = boto.ec2.connect_to_region('us-east-1',
	aws_access_key_id=aws_access_key_id,
	aws_secret_access_key=aws_secret_access_key) #return type boto.ec2.connection.EC2Connection

#conn.delete_key_pair('key_pair') # deleting key_pair, in case a duplicate exists
key_pair = conn.create_key_pair('key_pair') #return type boto.ec2.keypair.KeyPair
key_pair.save('.')

#conn.delete_security_group('csc326-group28')	# deleting security group, in case a duplicate exists
security_group = conn.create_security_group('csc326-group28','Instance for hosting web application') #return typeboto.ec2.securitygroup.SecurityGroup
security_group.authorize('ICMP', -1, -1, '0.0.0.0/0')	#ping server
security_group.authorize('TCP', 22, 22, '0.0.0.0/0')	#allow SSH
security_group.authorize('TCP', 80, 80, '0.0.0.0/0')	#allow HTTP

#conn.terminate(instance.Instace)
instance = conn.run_instances(image_id='ami-8caa1ce4',
	key_name='key_pair',
	security_groups=['csc326-group28'],
	instance_type='t1.micro')
