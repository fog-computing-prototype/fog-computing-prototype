#!/bin/sh
. ./gcp-00-settings.sh

if [ -f $CREDENTIAL_PATH_PUB ]; then
    echo "SSH already exists"
else
    echo "Create new SSH key in: '$CREDENTIAL_PATH'"
    ssh-keygen \
        -t rsa \
        -f $CREDENTIAL_PATH \
        -P $SSH_PW \
        -C $COMMENT_SSH \
        -b 2048
fi

echo ""

# Select GCP project
echo "Select GCP project:"
echo "--------------------------------------"
gcloud config \
    set project $PROJECT_ID
echo "--------------------------------------"
echo ""

# Add SSH key to GCP project
echo "Add SSH key to GCP project:"
echo "--------------------------------------"
gcloud compute \
    project-info \
    add-metadata \
    --metadata-from-file=ssh-rsa=$CREDENTIAL_PATH_PUB
echo "--------------------------------------"
echo ""

gcloud compute \
    firewall-rules \
    create $FIREWALL_RULES_NAME \
    --allow=icmp,tcp:22,tcp:5556,tcp:8000 \
    --target-tags=$GCP_TAGS

# Create GCP compute instance
echo "Create GCP compute instance: $COMPUTE_ENGINE_INSTANCE_NAME:"
echo "--------------------------------------"
gcloud compute \
    instances \
    create $COMPUTE_ENGINE_INSTANCE_NAME \
    --image=$COMPUTE_ENGINE_IMAGE \
    --metadata-from-file=ssh-rsa=$CREDENTIAL_PATH_PUB \
    --image-project=$COMPUTE_ENGINE_IMAGE_PROJECT \
    --zone=$GCP_ZONE \
    --machine-type=$COMPUTE_ENGINE_MACHINE_TYPE \
    --tags=$GCP_TAGS
echo "--------------------------------------"
echo ""
