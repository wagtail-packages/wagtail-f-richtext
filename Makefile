run:
	@echo "Running sandbox..."
	python manage.py runserver 0:8000
	
test:
	python manage.py test

tox:
	tox --skip-missing-interpreters

migrate:
	python manage.py migrate

dumpdata:
	python manage.py shell -c "from wagtail.images.models import Rendition; Rendition.objects.all().delete()"
	python manage.py dumpdata --natural-foreign --indent 2 \
    -e contenttypes -e auth.permission \
    -e wagtailcore.groupcollectionpermission \
    -e wagtailcore.grouppagepermission -e wagtailimages.rendition \
	-e wagtailcore.collection \
	-e wagtailcore.referenceindex \
	-e wagtailcore.workflow \
	-e wagtailcore.workflowtask \
	-e wagtailcore.workflowpage \
	-e wagtailcore.task \
    -e sessions > wagtail_f_richtext/test/fixtures/data.json

loaddata:
	python manage.py loaddata wagtail_f_richtext/test/fixtures/data.json
	mkdir -p wagtail_f_richtext/test/media/original_images
	chmod -R 775 wagtail_f_richtext/test/media/original_images
	cp -r wagtail_f_richtext/test/fixtures/original_images/* wagtail_f_richtext/test/media/original_images/
