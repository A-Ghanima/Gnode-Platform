.PHONY: help
.PHONY: status


help: ## Show available commands
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

status: ## Show status of all stacks
	@for dir in apps/* bots/* infrastructure/* monitoring/; do \
		echo "=== $$dir ==="; \
		cd $$dir && docker compose ps 2>/dev/null; cd -; \
	done
