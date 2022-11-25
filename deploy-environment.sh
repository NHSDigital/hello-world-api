#!/bin/bash

if [ -z "$ENVIRONMENT" ]
then
    export TITLE="Hello World API"
    export ENVIRONMENT="sandbox"
else
    export TITLE="Hello World API - $ENVIRONMENT"
fi

make publish

curl -X PUT "https://proxygen.ptl.api.platform.nhs.uk/apis/$PROXYGEN_API_NAME/environments/$ENVIRONMENT/instances/$INSTANCE" \
    -H "Authorization: $(proxygen get-token)" \
    -H 'Content-Type: application/json' \
    -d @build/hello-world-rendered.json \
    --fail
