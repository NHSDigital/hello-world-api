#!/bin/bash

if [ -z "$PR_NUMBER" ]
then
    instance=$ENVIRONMENT
else
    instance=$ENVIRONMENT-$PR_NUMBER
fi
export INSTANCE=$instance

instance_payload=$( envsubst < deployment.json )

curl -X POST https://proxygen.ptl.api.platform.nhs.uk/apis/hello-paas/instances?apply=true \
-H "Authorization: Bearer ${PROXYGEN_TOKEN}" \
-H "Content-Type: application/json" \
-d "$instance_payload"
