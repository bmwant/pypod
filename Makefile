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
