SHELL=/bin/bash -euo pipefail

install: install-node install-python install-hooks

install-python:
	poetry install

install-node:
	npm install
	cd docker/hello-world-sandbox && npm install && cd ../../tests && npm install

install-hooks:
	cp scripts/pre-commit .git/hooks/pre-commit

test:
	npm run test

lint:
	npm run lint
	cd docker/hello-world-sandbox && npm run lint && cd ..
	find . -name '*.py' | xargs poetry run flake8

publish:
	npm run publish 2> /dev/null

serve: update-examples
	npm run serve

clean:
	rm -rf build
	rm -rf dist

generate-examples: publish
	mkdir -p build/examples
	poetry run python scripts/generate_examples.py build/hello-world.json build/examples

update-examples: generate-examples
	jq -rM . <build/examples/resources/Greeting.json >specification/components/examples/Greeting.json
	make publish

check-licenses:
	npm run check-licenses
	scripts/check_python_licenses.sh

deploy-proxy: update-examples
	scripts/deploy_proxy.sh

deploy-spec: update-examples
	scripts/deploy_spec.sh

format:
	poetry run black **/*.py


build-proxy:
	scripts/build_proxy.sh

release: clean publish build-proxy
	mkdir -p dist
	tar -zcvf dist/package.tar.gz build
	cp ecs-proxies-deploy.yml dist/ecs-deploy-all.yml
	cp -r build/. dist
	cp -r tests dist
	cp -r api_tests dist

sandbox: update-examples
	cd docker/hello-world-sandbox && npm run start


