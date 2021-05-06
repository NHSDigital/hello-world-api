SERVICE_BASE_PATH ?= hello-world
PYTEST_ARGS = --service_base_path $(SERVICE_BASE_PATH) --apigee_env internal-dev --client_id eAMbFALgZFdnds2w5Z1u78AGCcJ0FtxQ \
	   --api_key=${API_KEY} --status_api_key=${STATUS_API_KEY} \
       --jwt_private_key_file $(shell pwd)/.env/jwtRS512.key \
       --id_token_private_key_file $(shell pwd)/.env/nhs_login.key

test:
	./venv/bin/pytest $(PYTEST_ARGS)

docker-build:
	docker build -t nhsd-apim/api-test .

docker-run:
	docker run --rm -it -v $(shell pwd)/.env:/var/api_tests/.env -v $(shell pwd)/reports:/var/api_tests/reports \
nhsd-apim/api-test:latest $(PYTEST_ARGS)
