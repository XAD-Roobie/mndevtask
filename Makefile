.PHONY: test
test:
	PYTHONPATH=. pytest

.PHONY: test_cov
test_cov:
	PYTHONPATH=. coverage run -m pytest; coverage report

.PHONY: init_db
init_db:
	python3 init_db.py

.PHONY: run
run:
	flask --app main.py run -h 0.0.0.0 -p 1337
