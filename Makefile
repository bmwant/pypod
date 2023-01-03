.PHONY: run
run:
	@poetry run pypod assets

.PHONY: debug
debug:
	@poetry run textual run --dev pypod/app.py:app

.PHONY: console
console:
	@poetry run textual console

.PHONY: dist
dist:
	@rm -rf dist/
	@rm -rf build/
	@poetry build

.PHONY: publish
publish:
	@poetry publish

.PHONY: isort
isort:
	@poetry run isort .

.PHONY: black
black:
	@poetry run black .

.PHONY: lint
lint:
	@poetry run flake8 .

.PHONY: changelog
changelog:
	@poetry run semantic-release changelog --unreleased

.PHONY: print-next-version
print-next-version:
	@poetry run semantic-release print-version --next
