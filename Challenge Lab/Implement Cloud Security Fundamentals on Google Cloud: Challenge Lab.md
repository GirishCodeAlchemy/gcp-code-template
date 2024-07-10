## `Lab Name` - *Implement Cloud Security Fundamentals on Google Cloud: Challenge Lab || GSP342||*

* ### Run the following Commands in CloudShell
```
export CUSTOM_SECURIY_ROLE=orca_storage_editor_xxx
```
```
export SERVICE_ACCOUNT=orca-private-cluster-xxx-sa
```

```
export CLUSTER_NAME=orca-cluster-xxx
```
```
export ZONE=us-central1-c
```
```
export REGION=us-central1
```

## Task 1. Create a custom security role

```
gcloud config set compute/zone $ZONE

cat > role-definition.yaml <<EOF_END
title: "$CUSTOM_SECURIY_ROLE"
description: "Permissions"
stage: "ALPHA"
includedPermissions:
- storage.buckets.get
- storage.objects.get
- storage.objects.list
- storage.objects.update
- storage.objects.create
EOF_END
```
```
gcloud iam service-accounts create orca-private-cluster-sa --display-name "Orca Private Cluster Service Account"
gcloud iam roles create $CUSTOM_SECURIY_ROLE --project $DEVSHELL_PROJECT_ID --file role-definition.yaml
```


## Task 2. Create a service account

```
gcloud iam service-accounts create $SERVICE_ACCOUNT --display-name "Orca Private Cluster Service Account"
```

## Task 3. Bind a custom security role to a service account

```
gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID --member serviceAccount:$SERVICE_ACCOUNT@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com --role roles/monitoring.viewer

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID --member serviceAccount:$SERVICE_ACCOUNT@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com --role roles/monitoring.metricWriter

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID --member serviceAccount:$SERVICE_ACCOUNT@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com --role roles/logging.logWriter

gcloud projects add-iam-policy-binding $DEVSHELL_PROJECT_ID --member serviceAccount:$SERVICE_ACCOUNT@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com --role projects/$DEVSHELL_PROJECT_ID/roles/$CUSTOM_SECURIY_ROLE
```

## Task 4. Create and configure a new Kubernetes Engine private cluster

You must now use the service account you have configured when creating a new Kubernetes Engine private cluster. The new cluster configuration must include the following:

- The cluster must be called orca-cluster-xxx
- The cluster must be deployed to the subnet orca-build-subnet
- The cluster must be configured to use the orca-private-cluster-xxx-sa service account.
- The private cluster options enable-master-authorized-networks, enable-ip-alias, enable-private-nodes, and enable-private-endpoint must be enabled.
- Once the cluster is configured you must add the internal ip-address of the orca-jumphost compute instance to the master authorized network list.


```
gcloud container clusters create $CLUSTER_NAME --num-nodes 1 --master-ipv4-cidr=172.16.0.64/28 --network orca-build-vpc --subnetwork orca-build-subnet --enable-master-authorized-networks  --master-authorized-networks 192.168.10.2/32 --enable-ip-alias --enable-private-nodes --enable-private-endpoint --service-account $SERVICE_ACCOUNT@$DEVSHELL_PROJECT_ID.iam.gserviceaccount.com --zone $ZONE
```

## Task 5. Deploy an application to a private Kubernetes Engine cluster

```
sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin
echo "export USE_GKE_GCLOUD_AUTH_PLUGIN=True" >> ~/.bashrc
source ~/.bashrc
gcloud container clusters get-credentials $CLUSTER_NAME --internal-ip --project=$DEVSHELL_PROJECT_ID --zone $ZONE
```

```
gcloud compute ssh --zone "$ZONE" "orca-jumphost" --project "$DEVSHELL_PROJECT_ID" --quiet --command "gcloud config set compute/zone $ZONE && gcloud container clusters get-credentials $CLUSTER_NAME --internal-ip && sudo apt-get install google-cloud-sdk-gke-gcloud-auth-plugin && kubectl create deployment hello-server --image=gcr.io/google-samples/hello-app:1.0 && kubectl expose deployment hello-server --name orca-hello-service --type LoadBalancer --port 80 --target-port 8080"
```

# Congratulations ..!! You completed the lab shortly..😃💯
