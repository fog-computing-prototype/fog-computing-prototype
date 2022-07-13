#!/bin/sh
. ./gcp-00-settings.sh

# Script to install Python 3.9 and poetry on VM

# Update apt
echo "Execute ssh command on compute instance:"
echo "sudo apt update"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "sudo apt update"
echo "--------------------------------------"
echo ""

# Prepare to install Python 3.9
echo "Execute ssh command on compute instance:"
echo "sudo apt install software-properties-common"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "sudo apt install software-properties-common"
echo "--------------------------------------"
echo ""

echo "Execute ssh command on compute instance:"
echo "sudo add-apt-repository ppa:deadsnakes/ppa"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "sudo add-apt-repository ppa:deadsnakes/ppa"
echo "--------------------------------------"
echo ""

echo "Execute ssh command on compute instance:"
echo "sudo apt update"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "sudo apt update"
echo "--------------------------------------"
echo ""

# Install Python 3.9
echo "Execute ssh command on compute instance:"
echo "sudo apt install python3.9"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "sudo apt install python3.9 -y"
echo "--------------------------------------"
echo ""

echo "Execute ssh command on compute instance:"
echo "python3.9 -V"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "python3.9 -V"
echo "--------------------------------------"
echo ""

# Install poetry for Python 3.9
echo "Execute ssh command on compute instance:"
echo "curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3.9 -"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3.9 -"
echo "--------------------------------------"
echo ""

echo "Execute ssh command on compute instance:"
echo "sudo apt-get install python3.9-distutils -y"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "sudo apt-get install python3.9-distutils -y"
echo "--------------------------------------"
echo ""

echo "Execute ssh command on compute instance:"
echo "sudo apt-get install python3-apt -y"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "sudo apt-get install python3-apt -y"
echo "--------------------------------------"
echo ""

echo "Execute ssh command on compute instance:"
echo "source /home/${USER_NAME}/.poetry/env"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "source /home/${USER_NAME}/.poetry/env"
echo "--------------------------------------"
echo ""

echo "Execute ssh command on compute instance:"
echo "poetry --version"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "source /home/${USER_NAME}/.poetry/env && poetry --version"
echo "--------------------------------------"
echo ""
