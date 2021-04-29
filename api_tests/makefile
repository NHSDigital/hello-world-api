test:
	./venv/bin/pytest --service_name hello-world --apigee_env internal-dev --client_id eAMbFALgZFdnds2w5Z1u78AGCcJ0FtxQ \
--jwt_private_key_file /Users/jhosseini/iw/nhs/nhsd-test-framework/.env/jwtRS512.key \
--id_token_private_key_file /Users/jhosseini/iw/nhs/nhsd-test-framework/.env/nhs_login.key

docker-build:
	docker build -t nhsd-apim/api-test .

docker-run:
	docker run --rm -it -v $(shell pwd)/.env:/var/api_tests/.env -v $(shell pwd)/reports:/var/api_tests/reports \
nhsd-apim/api-test:latest \
--service_name hello-world --apigee_env internal-dev \
--client_id eAMbFALgZFdnds2w5Z1u78AGCcJ0FtxQ \
--jwt_private_key_file /var/api_tests/.env/jwtRS512.key \
--id_token_private_key_file /var/api_tests/.env/nhs_login.key
