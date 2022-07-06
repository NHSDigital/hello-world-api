SERVICE_BASE_PATH ?= hello-world
PYTEST_ARGS = --service_base_path $(SERVICE_BASE_PATH) --apigee_env internal-dev --client_id=${API_KEY} \
	   --api_key=${API_KEY} --status_api_key=${STATUS_API_KEY} \
       --jwt_private_key_file $(shell pwd)/jwtRS512.key \
       --id_token_private_key_file $(shell pwd)/jwtRS512.key \
	   --oauth_token_endpoint https://internal-dev.api.service.nhs.uk/oauth2/token

test:
	./venv/bin/pytest $(PYTEST_ARGS)

docker-build:
	docker build -t nhsd-apim/api-test .

docker-run:
	docker run --rm -it -v $(shell pwd)/.env:/var/api_tests/.env -v $(shell pwd)/reports:/var/api_tests/reports \
nhsd-apim/api-test:latest $(PYTEST_ARGS)

-include .env

.EXPORT_ALL_VARIABLES:

run:
	poetry run pytest -s -v $(PYTEST_ARGS) $(f);

#  run tests with certain marker e.g. make run-sandbox runs tests marked with sandbox
run-%:
	poetry run pytest -s -v -m "$*" $(f)
