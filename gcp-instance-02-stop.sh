#!/bin/sh
. ./gcp-00-settings.sh

gcloud compute \
    instances \
    stop \
    $COMPUTE_ENGINE_INSTANCE_NAME \
    --zone $GCP_ZONE
