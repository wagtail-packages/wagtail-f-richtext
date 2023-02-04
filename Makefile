run:
	python manage.py runserver 0:8000
	
test:
	python manage.py test

tox:
	tox --skip-missing-interpreters

migrate:
	python manage.py migrate

superuser:
	@echo "from django.contrib.auth import get_user_model; get_user_model().objects.create_superuser('admin', '', 'admin')" | python manage.py shell
