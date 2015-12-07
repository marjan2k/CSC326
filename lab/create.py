import boto.ec2
import subprocess
import time
import sys

key_pair_name = 'key_pair_test'

def create():
	#key_pair_name = 'key_pair'

	#open the file containing credentials and reads lines
	try:
		with open ('credentials.csv', 'r') as f:
			lines = f.readlines()
	except Exception as exception:
		print "Exception returned: ", exception
		return NULL

	#print lines[1:]

	user = 1#int(raw_input("Instance Admin? (Choose number)\n[1] Ismail\n[2] Zen\n[3] Marjan\n--> "))
	aws_user_info = lines[user].split(',')
	aws_access_key_id = aws_user_info[1].strip()
	aws_secret_access_key = aws_user_info[2].strip()
	# print aws_user_info
	# print aws_access_key_id
	# print aws_secret_access_key

	#Create connection
	conn = boto.ec2.connect_to_region('us-east-1',
	aws_access_key_id=aws_access_key_id,
	aws_secret_access_key=aws_secret_access_key)

	#Create a key pair value and save it
	try:
		key_pair = conn.create_key_pair(key_pair_name)
		key_pair.save('.')
	except Exception as exception:
		print "Exception returned: ", exception

	#Create Security Group
	try:
		security_group = conn.create_security_group('csc326-group28-test','Test instance to host web server') #return typeboto.ec2.securitygroup.SecurityGroup
	except Exception as exception:
		for i in conn.get_all_security_groups():
			if i.name == 'csc326-group28':
				security_group = i
		print "Exception returned: ", exception

	#Protocols
	try:
		security_group.authorize('ICMP', -1, -1, '0.0.0.0/0')	#ping server
		security_group.authorize('TCP', 22, 22, '0.0.0.0/0')	#allow SSH
		security_group.authorize('TCP', 80, 80, '0.0.0.0/0')	#allow HTTP
		security_group.authorize('TCP', 8080, 8080, '0.0.0.0/0')#custom port
	except Exception as exception:
		print "Exception returned: ", exception

	#Start a new instance
	instance_reservation = conn.run_instances(image_id='ami-8caa1ce4',
	key_name=key_pair_name,
	security_groups=[security_group.name],
	instance_type='t1.micro')

	instance = instance_reservation.instances[0]

	print "Waiting for instance to be ready.."
	while instance.update() != 'running':
		time.sleep(5)

	print "Instance is running"
	time.sleep(1)

	print "Waiting for server to be stable.."
	for i in range(60,0,-1):
		time.sleep(1)
		sys.stdout.write(str(i)+' ')
    	sys.stdout.flush()

	subprocess.call("scp -i %s.pem -o StrictHostKeyChecking=no install.sh ubuntu@%s:~/" % (key_pair_name, instance.ip_address), shell=True)
	print "scp'd. now moving on to running the script"
	subprocess.Popen(("ssh -i %s.pem ubuntu@%s /bin/bash ~/install.sh" % (key_pair_name, instance.ip_address)).split())
	# subprocess.Popen(("ssh -i %s.pem ubuntu@%s ./install.sh" % (key_pair_name, instance.ip_address)).split())
	print "running script on remote server.."

	print "Search engine will be running on %s:8080" % instance.ip_address
	print "Instance ID and Instance IP address: (%s, %s)" % (instance.id, instance.ip_address)
	print "Instance ID and public IP returned. Setting up environment tools and dependencies for the server on the host machine"
	return (instance.id, instance.ip_address)




if __name__ == '__main__':
	create()