#!/bin/sh
. ./gcp-00-settings.sh

# Script to upload files and install dependencies

TEMP_FOLDER_PATH="${TEMP_FOLDER_NAME}/"

if [ -f $TEMP_FOLDER_PATH ]; then
    rm -r $TEMP_FOLDER_PATH
else
    .
fi

# Copy files to a temp dir and exclude unnecessary files
echo "Copy files to temp folder: '$TEMP_FOLDER_PATH':"
echo "--------------------------------------"
rsync -a \
    --exclude ".vscode/" \
    --exclude "tests/" \
    --exclude "__pycache__/" \
    --exclude "*.db" \
    --exclude "*.rst" \
    --exclude "README.rst" \
    cloud/ .cloud-temp/
echo "--------------------------------------"
echo ""

# Delete folder on VM
echo "Execute ssh command on compute instance:"
echo "rm -rf $DESTINATION_PATH"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "rm -rf $DESTINATION_PATH"
echo "--------------------------------------"
echo ""

echo "Copy code from local machine to the remote vm:"
echo "--------------------------------------"
gcloud compute \
    scp \
    --recurse \
    $TEMP_FOLDER_PATH \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}:$DESTINATION_PATH" \
    --zone=$GCP_ZONE
echo "--------------------------------------"
echo ""

# Install project dependencies
echo "Execute ssh command on compute instance:"
echo "source /home/${USER_NAME}/.poetry/env && cd $DESTINATION_PATH && poetry install --no-dev"
echo "--------------------------------------"
gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "source /home/${USER_NAME}/.poetry/env && cd $DESTINATION_PATH && poetry install --no-dev"
echo "--------------------------------------"
echo ""
