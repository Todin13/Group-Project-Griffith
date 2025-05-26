prepare:
	@echo "Preparing the set up"
	poetry config virtualenvs.prefer-active-python true
	poetry config virtualenvs.in-project true
	poetry install --no-root

run:
	@echo "Starting the app"
	poetry run python code/main.py

splitting:
	@echo "Starting the splitting"
	poetry run python 

check:
	@echo "Running Black"
	poetry run black --check .
	@echo "Running Vulture"
	poetry run vulture main.py
	@echo ""
	@echo "All goods !!!"

style:
	poetry run black .
