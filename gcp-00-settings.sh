#!/bin/sh

if [ -f "./credential.sh" ]; then
    . ./credential.sh
else
    echo "Credentials file not exist! Look in the 'README.rst' to setup the file correctly."
    exit
fi

# GCP settings
# Regions and zones 
GCP_ZONE="europe-west2-c"
GCP_TAGS="fog-computing"

# GCP compute engine
# Freely selectable name for the instance
COMPUTE_ENGINE_INSTANCE_NAME="fc-compute-instance"
COMPUTE_ENGINE_IMAGE="ubuntu-1804-bionic-v20220616"
COMPUTE_ENGINE_IMAGE_PROJECT="ubuntu-os-cloud"
COMPUTE_ENGINE_MACHINE_TYPE="e2-micro"

# GCP firewall
# Freely selectable name for the instance firewall
FIREWALL_RULES_NAME="fcrules"

# SSH variables
CREDENTIAL_PATH="${CREDENTIALS_PATH}/${CREDENTIAL_NAME}"
CREDENTIAL_PATH_PUB="${CREDENTIALS_PATH}/${CREDENTIAL_NAME}.pub"

# Remote VM
TEMP_FOLDER_NAME=".cloud-temp"
DESTINATION_PATH="/home/${USER_NAME}/cloud"
