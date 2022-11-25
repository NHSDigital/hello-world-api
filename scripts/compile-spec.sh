#!/bin/bash

export ref='$ref'
mkdir -p build
envsubst < specification/hello-world.yaml > build/hello-world-populated.yaml
node_modules/.bin/speccy resolve build/hello-world-populated.yaml -i | poetry run python scripts/yaml2json.py > build/hello-world-rendered.json
