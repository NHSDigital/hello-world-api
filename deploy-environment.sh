#!/bin/bash
api_name="hello-world"

if [ -z "$PR_NUMBER" ]
then
    instance=$ENVIRONMENT
    base_path=$api_name
else
    instance=$ENVIRONMENT-pr-$PR_NUMBER
    base_path=$api_name-pr-$PR_NUMBER
fi
echo $instance
export INSTANCE=$instance
export BASE_PATH=$base_path

instance_payload=$( envsubst < deployment.json )

curl -X POST https://proxygen.ptl.api.platform.nhs.uk/apis/$api_name/instances?apply=true \
-H "Authorization: Bearer ${PROXYGEN_TOKEN}" \
-H "Content-Type: application/json" \
-d "$instance_payload"
