prepare:
	@echo "Preparing the set up"
	poetry config virtualenvs.prefer-active-python true
	poetry config virtualenvs.in-project true
	poetry install --no-root

run:
	@echo "Starting the app"
	poetry run python src/main.py

pinecone-populate:
	poetry run python src/pinecone/init_rag_db.py

pinecone-purge:
	poetry run python src/pinecone/delete_rag_db.py

faiss-populate:
	poetry run python src/faiss/init_rag_db.py

faiss-purge:
	poetry run python src/faiss/delete_rag_db.py

data-transfo:
	pdftotext Griffith\ College\ 200\ Years.pdf
	./src/pdf_manipulation/pdf_to_chunk.sh

check:
	@echo "Running Black"
	poetry run black --check .
	@echo "Running Vulture"
	poetry run vulture main.py
	@echo ""
	@echo "All goods !!!"

style:
	poetry run black .

login:
	poetry run huggingface-cli login