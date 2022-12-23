# Hello World API

![Build](https://github.com/NHSDigital/hello-world-api/workflows/Build/badge.svg?branch=master)

[![apigee-release-pipeline](https://github.com/NHSDigital/hello-world-api/actions/workflows/apigee-release-pipeline.yml/badge.svg?branch=master)](https://github.com/NHSDigital/hello-world-api/actions/workflows/apigee-release-pipeline.yml)

[![spec-release-pipeline](https://github.com/NHSDigital/hello-world-api/actions/workflows/spec-release-pipeline.yml/badge.svg?branch=master)](https://github.com/NHSDigital/hello-world-api/actions/workflows/spec-release-pipeline.yml)

This is a RESTful HL7® FHIR® API specification for the *Hello World API*.

The *Hello World API* is the first API to use API Management's Proxygen service to deploy using API calls. For more see [Deployment](#Deployment).

* `specification/` This [Open API Specification](https://swagger.io/docs/specification/about/) describes the endpoints, methods and messages exchanged by the API. Use it to generate interactive documentation; the contract between the API and its consumers. The specification also includes a `x-nhsd-apim` metadata item that describes servers the API rests on.
* `sandbox/` This NodeJS application implements a mock implementation of the service. Use it as a back-end service to the interactive documentation to illustrate interactions and concepts. It is not intended to provide an exhaustive/faithful environment suitable for full development and testing.
* `scripts/` Utilities helpful to developers of this specification.

Consumers of the API will find developer documentation on the [NHS Digital Developer Hub](https://digital.nhs.uk/developer/api-catalogue/hello-world).

## Table of Contents
1. [Contributing](#Contributing)
2. [Deployment](#Deployment)
3. [Development](#Development)

## Contributing
Contributions to this project are welcome from anyone, providing that they conform to the [guidelines for contribution](https://github.com/NHSDigital/hello-world-api/blob/master/CONTRIBUTING.md) and the [community code of conduct](https://github.com/NHSDigital/hello-world-api/blob/master/CODE_OF_CONDUCT.md).

### Licensing
This code is dual licensed under the MIT license and the OGL (Open Government License). Any new work added to this repository must conform to the conditions of these licenses. In particular this means that this project may not depend on GPL-licensed or AGPL-licensed libraries, as these would violate the terms of those libraries' licenses.

The contents of this repository are protected by Crown Copyright (C).

## Deployment

### Proxygen

Hello World is the first API to use API Management's Proxygen to deploy the proxy, products, sandbox and spec through API calls.

The Proxygen API calls are handled by the Proxygen CLI 

Proxygen uses the OAS specification in `specification/hello-world.yaml` to inform the exact details on resource names and behaviours.

The deployments use Github actions to deploy the API. These pipelines are found in the `.github/workflows` directory and can be monitored under the ['Actions'](https://github.com/NHSDigital/hello-world-api/actions) tab in the GitHub repo.

### Apigee release pipeline
The `apigee-release-pipeline.yml` builds and pushes the docker image of the sandbox to ECS using Proxygen's docker authentication, then makes API calls to Proxygen using the Proxygen CLI for each environment using data provided in the specification. After that it is configured to run end-to-end tests for any internal environments deployed. As Hello World is not a real API, it only deploys to sandbox environments.

#### Pull requests
On pushes to branches with a pull request the pipeline is configured to append the pr number to the instances deployed and only deploy to internal environments. This means it's possible to develop code against pr versions of the API.

### Spec release pipeline

The `spec-release-pipeline.yml` will publish the spec using the Proxygen CLI. The CLI will do variable substitution and build up the spec file. The proxygen server will ensure the spec file is valid before publishing it. When Proxygen deploys a spec it bypasses Apigee and is held in an S3 bucket which Bloomreach is configured to pull from and then update the [NHS Digital Developer Hub](https://digital.nhs.uk/developer/api-catalogue/hello-world).

#### Pull requests
On pushes to branches with a pull request the pipeline is configured to only lint the spec.

## Development

### Requirements
* make
* nodejs + npm/yarn
* [poetry](https://github.com/python-poetry/poetry)

### Install
```
$ make install
```

### Environment Variables
Various scripts and commands rely on environment variables being set. These are documented with the commands.

:bulb: Consider using [direnv](https://direnv.net/) to manage your environment variables during development and maintaining your own `.envrc` file - the values of these variables will be specific to you and/or sensitive.

### Make commands
There are `make` commands that alias some of this functionality:

Make sure you have run `make install` [here](###Install).

 * `lint` -- Lints the spec and code
 * `publish` -- Outputs the specification as a **single file** into a `build/` directory
 * `serve` -- Serves a preview of the specification in human-readable format
 * `generate-examples` -- generate example objects from the specification

### Running tests

Hello World using API Management's `pytest-nhsd-apim` python extension to easily authenticate with our Authorisation service and make calls against the proxy. See [the repo](https://github.com/NHSDigital/pytest-nhsd-apim) for how to use for further development.

To run tests, run `make install` and ensure you have the following environment variables set:
```
     # This must be set as an environment variable
     export API_NAME="hello-world"

     # append your pr number if testing a pr e.g. "internal-dev-sandbox-303"
     export INSTANCE="internal-dev-sandbox"

     # See below
     export APIGEE_ACCESS_TOKEN=<your-apigee-access-token>
```
For information on using Apigee's `get_token` see [here](https://docs.apigee.com/api-platform/system-administration/using-gettoken#:~:text=The%20get_token%20utility%20lets%20you,an%20access%20or%20refresh%20token.)

Run the tests from the root of the repo using the following command:
```
poetry run pytest tests/api_tests.py
```
### VS Code Plugins

 * [openapi-lint](https://marketplace.visualstudio.com/items?itemName=mermade.openapi-lint) resolves links and validates entire spec with the 'OpenAPI Resolve and Validate' command
 * [OpenAPI (Swagger) Editor](https://marketplace.visualstudio.com/items?itemName=42Crunch.vscode-openapi) provides sidebar navigation


### Emacs Plugins

 * [**openapi-yaml-mode**](https://github.com/esc-emacs/openapi-yaml-mode) provides syntax highlighting, completion, and path help

### Speccy

> [Speccy](https://github.com/wework/speccy) *A handy toolkit for OpenAPI, with a linter to enforce quality rules, documentation rendering, and resolution.*

Speccy does the lifting for the following npm scripts:

 * `test` -- Lints the definition
 * `publish` -- Outputs the specification as a **single file** into the `dist/` directory
 * `serve` -- Serves a preview of the specification in human-readable format

(Workflow detailed in a [post](https://developerjack.com/blog/2018/maintaining-large-design-first-api-specs/) on the *developerjack* blog.)

:bulb: The `publish` command is useful for full expanding the spec, then sending to Proxygen, which requires the spec as a single file.

### Caveats

#### Swagger UI
Swagger UI unfortunately doesn't correctly render `$ref`s in examples, so use `speccy serve` instead.

#### Apigee Portal
The Apigee portal will not automatically pull examples from schemas, you must specify them manually.
