#!/bin/bash
api_name="hello-world"

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
    export TITLE="Hello World API - $instance"
fi

export BASE_PATH=$base_path
export SANDBOX_DOMAIN=$ENVIRONMENT

mkdir -p build && poetry run python scripts/yaml2json.py < specification/hello-world.yaml > build/hello-world.json
export ref="\$ref"
envsubst < build/hello-world.json > build/hello-world-tmp.json

curl -X PUT "https://proxygen.ptl.api.platform.nhs.uk/apis/$api_name/environments/$ENVIRONMENT/instances/$BASE_PATH" \
    -H "Authorization: $(proxygen get-token)" \
    -H 'Content-Type: application/json' \
    -d @build/hello-world-tmp.json \
    --fail
