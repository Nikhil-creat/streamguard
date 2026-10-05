up:
	docker compose up --build
seed:
	python rag/seed.py
test:
	pytest tests
