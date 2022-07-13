#!/bin/sh
. ./gcp-00-settings.sh

# Script to start cloud app

echo "Execute ssh command on compute instance:"
echo "source /home/${USER_NAME}/.poetry/env && cd $DESTINATION_PATH && poetry run uvicorn cloud.main:app"
echo "--------------------------------------"
nohup \
    gcloud beta compute \
    ssh \
    --zone $GCP_ZONE \
    "${USER_NAME}@${COMPUTE_ENGINE_INSTANCE_NAME}" \
    --project $PROJECT_ID \
    --command "source /home/${USER_NAME}/.poetry/env && cd $DESTINATION_PATH && poetry run uvicorn cloud.main:app --host 0.0.0.0 >> /home/${USER_NAME}/log_cloud.log" &
echo "--------------------------------------"
echo ""
