import boto.ec2
import os.path
import time


def main():

    KeyName = 'csc326-group36-keypair'
    GroupName = 'csc326-group36'


    connection = boto.ec2.connect_to_region(# hard code the user's credentials
        'us-east-1',
        aws_access_key_id = '********',
        aws_secret_access_key = '******',)
    
    # allocte ip address
    allocation = connection.allocate_address( domain = 'standard')
    #print allocation

    
    # create a key pair
    key_pair = connection.create_key_pair(KeyName)
    print "Create key pair: " + str(key_pair)

    # check whether the keyfile has already existed, if it has, delete it first
    if os.path.isfile (KeyName + '.pem'):
        os.remove(KeyName + '.pem')

    key_pair.save('.')


    # create a secturity group
    security_group = connection.create_security_group(GroupName, 'Secturity group for csc326')
    print "Create security group: " + str(security_group)

    # authorize folloewing protocols:
    data = security_group.authorize('icmp', -1, -1, '0.0.0.0/0')
    data = security_group.authorize('tcp', 22, 22, '0.0.0.0/0')
    data = security_group.authorize('tcp', 80, 80, '0.0.0.0/0')

    #print security_group.rules

    # start a new instance:
    Reservation = connection.run_instances(
        'ami-8caa1ce4',
        key_name = KeyName,
        security_groups = [GroupName],
        instance_type="t1.micro",)
    
    
    instance = Reservation.instances[0]
    
    # keep checking the instance status, until it becomes "running"
    while True:
        print "Loading the instance..."
        instance.update()
        if instance.state == 'running':
            break
        time.sleep(5)

    print "Instance: " + str(instance.id) + " is ready!!"

    # accociate this running instance with a IP address
    response = connection.associate_address(public_ip = allocation.public_ip, instance_id=instance.id)
    
    if response:
        print "Associate IP: " + str(allocation.public_ip) + " to instance " + str(instance.id) + "!"
    else: 
        print "IP Association failed!"

    print "Instance ip: " + str(instance.ip_address)
    return

if __name__ == "__main__": main()
