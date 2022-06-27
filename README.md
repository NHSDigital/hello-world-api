# hello-world-api

![Build](https://github.com/NHSDigital/hello-world-api/workflows/Build/badge.svg?branch=master)

This is a RESTful HL7® FHIR® API specification for the *Hello World API*.

* `specification/` This [Open API Specification](https://swagger.io/docs/specification/about/) describes the endpoints, methods and messages exchanged by the API. Use it to generate interactive documentation; the contract between the API and its consumers.
* `sandbox/` This NodeJS application implements a mock implementation of the service. Use it as a back-end service to the interactive documentation to illustrate interactions and concepts. It is not intended to provide an exhaustive/faithful environment suitable for full development and testing.
* `scripts/` Utilities helpful to developers of this specification.
* `proxies/` Live (connecting to another service) and sandbox (using the sandbox container) Apigee API Proxy definitions.

Consumers of the API will find developer documentation on the [NHS Digital Developer Hub](https://digital.nhs.uk/developer/api-catalogue/hello-world).

## Table of Contents
1. [Contributing](#Contributing)
2. [Development](#Development)
3. [Deployment](#Deployment)

## Contributing
Contributions to this project are welcome from anyone, providing that they conform to the [guidelines for contribution](https://github.com/NHSDigital/hello-world-api/blob/master/CONTRIBUTING.md) and the [community code of conduct](https://github.com/NHSDigital/hello-world-api/blob/master/CODE_OF_CONDUCT.md).

### Licensing
This code is dual licensed under the MIT license and the OGL (Open Government License). Any new work added to this repository must conform to the conditions of these licenses. In particular this means that this project may not depend on GPL-licensed or AGPL-licensed libraries, as these would violate the terms of those libraries' licenses.

The contents of this repository are protected by Crown Copyright (C).

## Development

### Requirements
* make
* nodejs + npm/yarn
* [poetry](https://github.com/python-poetry/poetry)

### Install
```
$ make install
```

#### Updating hooks
Some pre-commit hooks are installed as part of the install command above to ensure you can't commit invalid spec changes by accident. These are also run
in CI.

```
$ make install-hooks
```

### Environment Variables
Various scripts and commands rely on environment variables being set. These are documented with the commands.

:bulb: Consider using [direnv](https://direnv.net/) to manage your environment variables during development and maintaining your own `.envrc` file - the values of these variables will be specific to you and/or sensitive.

### Make commands
There are `make` commands that alias some of this functionality:

Make sure you have run `make install` [here](###Install).

 * `lint` -- Lints the spec and code
 * `publish` -- Outputs the specification as a **single file** into the `dist/` directory
 * `serve` -- Serves a preview of the specification in human-readable format
 * `generate-examples` -- generate example objects from the specification

### Running tests
#### End-to-end tests
To run tests, install virtual environment by using the following commands

pip install virtualenv
     virtualenv test_env
     source ./test_env/bin/activate
     pip install -r requirements.txt

Set the following environment variables in a .env file  for local testing:
 * `SERVICE_BASE_PATH`
 * `API_KEY`
 * `STATUS_API_KEY`
 * `jwtRS512.key`
 * `nhs_login.key`


In order for local tests to work, you must have the sandbox server running locally.
```
make sandbox
```

To run local tests, go to the api_test [/api_tests] folder:
```
make test
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

:bulb: The `publish` command is useful when uploading to Apigee which requires the spec as a single file.

### Caveats

#### Swagger UI
Swagger UI unfortunately doesn't correctly render `$ref`s in examples, so use `speccy serve` instead.

#### Apigee Portal
The Apigee portal will not automatically pull examples from schemas, you must specify them manually.

### Postman Collection

`Patient Demographics Sandbox.postman_collection` must be kept in sync with the OAS and Sandbox manually.

Procedure:
 * Import the collection into Postman
 * Update requests and export the collection back into the repo
 * Re-generate the [Run in Postman button](https://learning.getpostman.com/docs/postman-for-publishers/run-in-postman/creating-run-button/) Markdown button link and update the OAS

## Deployment

#### Environment variables

You need a apgiee account to deploy to apigee
* `APIGEE_USERNAME` - your apigee username
* `APIGEE_PASSWORD` - your apigee password

Navigate to develop/specs in the apigee ui and select the spec you want to update, the APIGEE_SPEC_ID is the last id in the url
.../specs/folder/.../editor/{APIGEE_SPEC_ID}
* `APIGEE_SPEC_ID`

Navigate to publish/portals
In chrome open the developer tools to monitor network traffic
For the portal that your spec belongs to click on "manage spec snapshot"
Then click "update snapshot" the APIGEE_PORTAL_API_ID will be the number in the network tab.
* `APIGEE_PORTAL_API_ID`

This is the value in the top left corner of the apigee web-console
* `APIGEE_ORGANIZATION`

Comma-separated list of environments to deploy to (e.g. `test,prod`)
* `APIGEE_ENVIRONMENTS`

Name of the API Proxy for deployment
* `APIGEE_APIPROXY`

The proxy's base path (must be unique)
* `APIGEE_BASE_PATH`

Name of the environment you are running tests against
* `ENVIRONMENT`

The base url of the proxy when deployed to apigee
* `API_TEST_URL`

### Github Deployment

Github uses Github actions to deploy the code to apigee. The Github action uses secrets to populate environment variables.
You need a Github secret for each environment variable. Each of the above environment variables need an equivalent secret in Github for
the deployment to work. These are pre-populated for you [here](https://github.com/NHSDigital/hello-world-api/settings/secrets/new). 
If you get a 404 for this page you will need to update your Github account permissions.

### Local Deployment

#### Specification
Update the API Specification and derived documentation in the Portal.

This will only allow you to update an existing spec, so you have to create the spec first using the apigee web console.

`make deploy-spec` with environment variables:

* `APIGEE_USERNAME`
* `APIGEE_PASSWORD`
* `APIGEE_SPEC_ID`
* `APIGEE_PORTAL_API_ID`

#### API Proxy & Sandbox Service
Redeploy the API Proxy and hosted Sandbox service.

If you use the same APIGEE_APIPROXY it will just create a new revision of the api proxy.

If you use the same APIGEE_BASE_PATH as an existing api proxy it will cause problems.

`make deploy-proxy` with environment variables:

* `APIGEE_USERNAME`
* `APIGEE_PASSWORD`
* `APIGEE_ORGANIZATION`
* `APIGEE_ENVIRONMENTS`
* `APIGEE_APIPROXY`
* `APIGEE_BASE_PATH`

:bulb: Specify your own API Proxy (with base path) for use during development.

#### Platform setup

Successful deployment of the API Proxy requires:

 1. A *Target Server* named `ig3`
 2. A *Key-Value Map* named `pds-variables`, containing:
    1. Key: `NHSD-ASID`, Value: Accredited System ID (ASID) identifying the API Gateway

:bulb: For Sandbox-running environments (`test`) these need to be present for successful deployment but can be set to empty/dummy values.
