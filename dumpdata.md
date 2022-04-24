# run the below command

```bash
python testmanage.py dumpdata --natural-foreign --indent 2 \
    -e contenttypes -e auth.permission \
    -e wagtailcore.groupcollectionpermission \
    -e wagtailcore.grouppagepermission -e wagtailimages.rendition \
    -e wagtailcore.pagerevision \
    -e sessions > wagtail_f_richtext/test/fixtures/test_data.json
```

# serach for `live_revision` 

and set to null for all pages