prepare:
	@echo "Preparing the set up"
	poetry config virtualenvs.prefer-active-python true
	poetry config virtualenvs.in-project true
	poetry install --no-root

run:
	@echo "Starting the app"
	poetry run python code/main.py

populate:
	poetry run python code/pinecone/init_rag_db.py

purge:
	poetry run python code/pinecone/delete_rag_db.py

data-transfo:
	./code/pdf_manipulation/pdf_to_chunk.sh

check:
	@echo "Running Black"
	poetry run black --check .
	@echo "Running Vulture"
	poetry run vulture main.py
	@echo ""
	@echo "All goods !!!"

style:
	poetry run black .
