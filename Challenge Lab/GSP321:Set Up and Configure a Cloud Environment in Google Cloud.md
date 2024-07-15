## `Lab Name` - *Set Up and Configure a Cloud Environment in Google Cloud: Challenge Lab || GSP321||*

![Environment](https://cdn.qwiklabs.com/UE5MydlafU0QvN7zdaOLo%2BVxvETvmuPJh%2B9kZxQnOzE%3D)


- Create a development VPC with three subnets manually
- Create a production VPC with three subnets manually
- Create a bastion that is connected to both VPCs
- Create a development Cloud SQL Instance and connect and prepare the WordPress environment
- Create a Kubernetes cluster in the development VPC for WordPress
- Prepare the Kubernetes cluster for the WordPress environment
- Create a WordPress deployment using the supplied configuration
- Enable monitoring of the cluster
- Provide access for an additional engineer

* ### Run the following Commands in CloudShell
```
export ZONE=us-east1-c
```
```
export REGION=us-east1
```
```
export DEV_VPC_NAME=griffin-dev-vpc
export PROD_VPC_NAME=griffin-prod-vpc
```
```
export DEV_MYSQL_INSTANCE=griffin-dev-db
```
```
export CLUSTER_NAME=griffin-dev
export MACHINE_TYPE=e2-standard-4
```

## Task 1. Create development VPC manually
```
gcloud compute networks create $DEV_VPC_NAME --subnet-mode=custom
gcloud compute networks subnets create griffin-dev-wp --network=$DEV_VPC_NAME --region=$REGION --range=192.168.16.0/20
gcloud compute networks subnets create griffin-dev-mgmt --network=$DEV_VPC_NAME --region=$REGION --range=192.168.32.0/20
```

## Task 2. Create production VPC manually
```
gcloud compute networks create $PROD_VPC_NAME --subnet-mode=custom
gcloud compute networks subnets create griffin-prod-wp --network=$PROD_VPC_NAME --region=$REGION --range=192.168.48.0/20
gcloud compute networks subnets create griffin-prod-mgmt --network=$PROD_VPC_NAME --region=$REGION --range=192.168.64.0/20
```

## Task 3. Create bastion host
```
gcloud compute instances create bastion-host \
    --zone=$ZONE --machine-type=n1-standard-1 --tags=ssh \
    --network-interface subnet=griffin-dev-mgmt \
    --network-interface subnet=griffin-prod-mgmt
```

```
gcloud compute firewall-rules create allow-tcp-dev --network=$DEV_VPC_NAME --allow=tcp:22 --source-ranges="0.0.0.0/0" --target-tags ssh
gcloud compute firewall-rules create allow-tcp-prod --network=$PROD_VPC_NAME --allow=tcp:22 --source-ranges="0.0.0.0/0" --target-tags ssh
```

## Task 4. Create and configure Cloud SQL Instance
```
gcloud sql instances create $DEV_MYSQL_INSTANCE --root-password password --region=$REGION
gcloud sql connect $DEV_MYSQL_INSTANCE
```

```
CREATE DATABASE wordpress;
CREATE USER "wp_user"@"%" IDENTIFIED BY "stormwind_rules";
GRANT ALL PRIVILEGES ON wordpress.* TO "wp_user"@"%";
FLUSH PRIVILEGES;
```

## Task 5. Create Kubernetes cluster
```
gcloud container clusters create $CLUSTER_NAME \
    --network $DEV_VPC_NAME --subnetwork=griffin-dev-wp \
    --zone=$ZONE --num-nodes=2 --machine-type=$MACHINE_TYPE
gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE
```

## Task 6. Prepare the Kubernetes cluster
```
gsutil cp -r gs://cloud-training/gsp321/wp-k8s .
cd wp-k8s
sed -i s/username_goes_here/wp_user/g wp-env.yaml
sed -i s/password_goes_here/stormwind_rules/g wp-env.yaml
kubectl apply -f wp-env.yaml
```

```
gcloud iam service-accounts keys create key.json \
    --iam-account=cloud-sql-proxy@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com
kubectl create secret generic cloudsql-instance-credentials \
    --from-file key.json
```

## Task 7. Create a WordPress deployment
```
INSTANCE_CONNECTION=$(gcloud sql instances describe $DEV_MYSQL_INSTANCE --format="value(connectionName)")
sed -i s/YOUR_SQL_INSTANCE/$INSTANCE_CONNECTION/g wp-deployment.yaml
kubectl apply -f wp-deployment.yaml
kubectl apply -f wp-service.yaml
```


## Task 8. Enable monitoring


Navigation Menu -> Kubernetes Engine -> Services and Ingress -> Copy Endpoint's address.

Navigation Menu -> Monitoring -> `Uptime Check` -> *`+Create Uptime Check`* 

   Title : `Wordpress Uptime`

Next -> Target
   Hostname : `<External IP of your wordpress db which you had got previously from this command *kubectl get svc -w*>`
   Path : `/`

Next -> Next -> *`Create`*


## Task 9. Provide access for an additional engineer
Navigation Menu -> IAM & Admin -> IAM -> *`+ GRANT ACCESS`*
New Member : {Username 2 from Lab instruction page}
Role : Project -> Editor
Save.

```
gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID --member=user:$USER_NAME2 --role=roles/editor
```

# Congratulations ..!! You completed the lab shortly..😃💯
