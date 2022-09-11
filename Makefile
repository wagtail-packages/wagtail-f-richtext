run:
	@echo "Running sandbox..."
	python sandbox/manage.py runserver 0:8000
	
test:
	python testmanage.py test

tox:
	tox --skip-missing-interpreters
