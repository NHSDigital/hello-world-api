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

envsubst < deployment.json > instance.json

proxygen apply