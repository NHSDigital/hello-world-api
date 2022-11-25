#!/bin/bash

export ref='$ref'
mkdir -p build
envsubst < specification/hello-world.yaml > build/hello-world-populated.yaml
cat build/hello-world-populated.yaml | poetry run python scripts/yaml2json.py > build/hello-world-rendered.json
