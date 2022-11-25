#!/bin/bash

if [ -z "$PR_NUMBER" ]
then
    export base_path=$api_name
else
    export base_path=$api_name-$PR_NUMBER
fi

if [ -z "$ENVIRONMENT" ]
then
    export TITLE="Hello World API"
    export ENVIRONMENT="sandbox"
else
    export TITLE="Hello World API - $ENVIRONMENT"
fi

mkdir -p build && poetry run python scripts/yaml2json.py < specification/hello-world.yaml > build/hello-world.json
export ref="\$ref"
envsubst < build/hello-world.json > build/hello-world-rendered.json

curl -X PUT "https://proxygen.ptl.api.platform.nhs.uk/apis/$PROXYGEN_API_NAME/environments/$ENVIRONMENT/instances/$INSTANCE" \
    -H "Authorization: $(proxygen get-token)" \
    -H 'Content-Type: application/json' \
    -d @build/hello-world-tmp.json \
    --fail
