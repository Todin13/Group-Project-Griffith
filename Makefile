prepare:
	@echo "Preparing the set up"
	poetry config virtualenvs.prefer-active-python true
	poetry config virtualenvs.in-project true
	poetry install --no-root

run:
	@echo "Starting the app"
	poetry run python -m src.main

pinecone-populate:
	poetry run python -m src.pinecone.init_rag_db

pinecone-purge:
	poetry run python -m src.pinecone.delete_rag_db

faiss-populate:
	poetry run python -m src.faiss.init_rag_db

faiss-purge:
	poetry run python -m src.faiss.delete_rag_db

data-transfo:
	mkdir -p data/griffith_img
	cd data && \
	pdftotext "Griffith College 200 Years.pdf" && \
	pdfimages -j "Griffith College 200 Years.pdf" griffith_img/Griffith_history && \
	../src/pdf_manipulation/pdf_to_chunk.sh

check:
	@echo "Running Black"
	poetry run black --check .
	@echo "Running Vulture"
	poetry run vulture src/main.py
	@echo ""
	@echo "All goods !!!"

style:
	poetry run black .

login:
	poetry run huggingface-cli login