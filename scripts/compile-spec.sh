#!/bin/bash

export ref='$ref'  # Make sure we retain $ref in the spec and not substitute it
mkdir -p build
envsubst < specification/hello-world.yaml > build/hello-world-populated.yaml
cat build/hello-world-populated.yaml | poetry run python scripts/yaml2json.py > build/hello-world-rendered.json
