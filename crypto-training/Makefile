.PHONY: docs-build docs-run docs-clean

docs-build:
@echo "Building Sphinx docs..."
@sphinx-build -b html docs/source docs/_build/html

docs-run:
@echo "Serving docs at http://localhost:1234"
@python3 -m http.server 1234 --directory docs/_build/html

docs-clean:
@echo "Cleaning docs build..."
@rm -rf docs/_build
