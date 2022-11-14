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
echo $instance
export INSTANCE=$instance
export BASE_PATH=$base_path

mkdir build -p && node_modules/.bin/speccy resolve sandbox-spec.yaml -i | poetry run python scripts/yaml2json.py | envsubst > build/hello-world.json

curl -X POST "https://proxygen.ptl.api.platform.nhs.uk/${{ api_name }}/environments/${{ ENVIRONMENT }}/instances/${{ INSTANCE }}" \
    -H "Authorization: $(proxygen get-token)" \
    -H 'Content-Type: application/json' \
    -d @build/hello-world.json
