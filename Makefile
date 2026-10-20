PORT ?= 8000

.PHONY: help serve test

help: ## List targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-8s %s\n", $$1, $$2}'

serve: ## Preview the page at http://127.0.0.1:$(PORT)/zipper-merge-lab.html
	python3 -m http.server $(PORT) --bind 127.0.0.1

test: ## Validate repository context and the page script
	@python3 scripts/check_repo_context.py
