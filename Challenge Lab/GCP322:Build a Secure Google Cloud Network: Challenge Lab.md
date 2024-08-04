## `Lab Name` - *Build a Secure Google Cloud Network: Challenge Lab|| [GSP322](https://www.cloudskillsboost.google/course_templates/654/labs/464661)||*

You need to create the appropriate security configuration for Jeff's site. Your first challenge is to set up firewall rules and virtual machine tags. You also need to ensure that SSH is only available to the bastion via IAP.

For the firewall rules, make sure that:

The bastion host does not have a public IP address.
You can only SSH to the bastion and only via IAP.
You can only SSH to juice-shop via the bastion.
Only HTTP is open to the world for juice-shop.

### Export all the values carefully

```bash
export SSH_IAP_NETWORK_TAG=accept-ssh-iap-ingress-ql-xxx

export SSH_INTERNAL_NETWORK_TAG=accept-ssh-internal-ingress-ql-xxx

export HTTP_NETWORK_TAG=accept-http-ingress-ql-xxx

export ZONE=europe-west1-b
```
###
###


### ***NOW JUST COPY THE CODE AND PASTE ON YOUR CLOUD SHELL***
###
###

1. Check the firewall rules. Remove the overly permissive rules.
```bash
gcloud compute firewall-rules delete open-access --quiet
```

2. Navigate to Compute Engine in the Cloud console and identify the bastion host. The instance should be stopped. Start the instance.

```bash
gcloud compute instances start bastion --zone=$ZONE --quiet
```

3. The bastion host is the one machine authorized to receive external SSH traffic. Create a firewall rule that allows SSH (tcp/22) from the IAP service. The firewall rule must be enabled for the bastion host instance using a network tag of accept-ssh-iap-ingress-ql-xxx.

```bash
gcloud compute firewall-rules create ssh-ingress --allow=tcp:22 --source-ranges 35.235.240.0/20 --target-tags $SSH_IAP_NETWORK_TAG --network acme-vpc --quiet

gcloud compute instances add-tags bastion --tags=$SSH_IAP_NETWORK_TAG --zone=$ZONE --quiet
```


4. The juice-shop server serves HTTP traffic. Create a firewall rule that allows traffic on HTTP (tcp/80) to any address. The firewall rule must be enabled for the juice-shop instance using a network tag of accept-http-ingress-ql-xxx

```bash
gcloud compute firewall-rules create allow-http --allow tcp:80 --source-ranges 0.0.0.0/0 --target-tags=$HTTP_NETWORK_TAG --network=acme-vpc --quiet

gcloud compute instances add-tags juice-shop --tags=$HTTP_NETWORK_TAG --zone=$ZONE --quiet

```

5. You need to connect to juice-shop from the bastion using SSH. Create a firewall rule that allows traffic on SSH (tcp/22) from acme-mgmt-subnet network address. The firewall rule must be enabled for the juice-shop instance using a network tag of accept-ssh-internal-ingress-ql-xxx.

```bash
gcloud compute firewall-rules create internal-ssh-ingress --allow tcp:22 --source-ranges=192.168.10.0/24 --target-tags=$SSH_INTERNAL_NETWORK_TAG --network=acme-vpc --quiet

gcloud compute instances add-tags juice-shop --tags=$SSH_INTERNAL_NETWORK_TAG --zone=$ZONE --quiet

```

### ***In Compute Engine -> VM Instances page, click the SSH button for the bastion host. Then SSH to juice-shop by:***



```bash

ssh 192.168.11.2 #Internal IP address of juice-shop

```

# Congratulations ..!! You completed the lab shortly..😃💯