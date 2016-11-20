.PHONY: test
test:
	coverage erase
	coverage run \
		--source=submitify,submitify/views,usermgmt_standalone \
		--omit='*migrations*,*urls.py,*apps.py,*admin.py,*__init__.py,*test.py' \
		manage.py test --verbosity=2
	coverage report -m --skip-covered