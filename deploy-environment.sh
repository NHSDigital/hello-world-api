#!/bin/bash
api_name="hello-world"

if [ -z "$PR_NUMBER" ]
then
    instance=$ENVIRONMENT
    base_path=$api_name
else
    instance=$ENVIRONMENT-$PR_NUMBER
    base_path=$api_name-$PR_NUMBER
fi

if [ -z "$ENVIRONMENT" ]
then
    export TITLE="Hello World API"
    ENVIRONMENT="sandbox"
else
    export TITLE="Hello World API - $instance"
fi

echo $instance
export INSTANCE=$instance
export BASE_PATH=$base_path
export SERVER_DOMAIN=$ENVIRONMENT

npm run publish
envsubst build/hello-world.json

curl -X PUT "https://proxygen.ptl.api.platform.nhs.uk/apis/$api_name/environments/$ENVIRONMENT/instances/$INSTANCE" \
    -H "Authorization: $(proxygen get-token)" \
    -H 'Content-Type: application/json' \
    -d @build/hello-world.json \
    --fail
