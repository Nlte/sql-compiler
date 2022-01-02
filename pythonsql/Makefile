default_target:help


.PHONY: help
help: ## show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: clean
clean: ## clean build files
	@find . -name '*.pyc' -delete
	@find . -name '*.pyo' -delete
	@find . -name '*__pycache__*' -delete
	@rm -rf build/
	@rm -rf dist/
	@rm -rf site/
	@rm -rf *.egg-info/

.PHONY: build
build: ## build distribution
	poetry build

.PHONY: test
test: ## run test suite
	poetry run pytest pythonsql

.PHONY: run
run: ## run main
	poetry run pythonsql-main
