SERVICE_NAME ?= hello-world
PYTEST_ARGS = --service_name $(SERVICE_NAME) --apigee_env internal-dev --client_id eAMbFALgZFdnds2w5Z1u78AGCcJ0FtxQ \
       --jwt_private_key_file $(shell pwd)/.env/jwtRS512.key \
       --id_token_private_key_file $(shell pwd)/.env/nhs_login.key

test:
	./venv/bin/pytest $(PYTEST_ARGS)

docker-build:
	docker build -t nhsd-apim/api-test .

docker-run:
	docker run --rm -it -v $(shell pwd)/.env:/var/api_tests/.env -v $(shell pwd)/reports:/var/api_tests/reports \
nhsd-apim/api-test:latest $(PYTEST_ARGS)
