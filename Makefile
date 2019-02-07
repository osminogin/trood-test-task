TESTHOST ?= http://localhost:8000

default: run

run:
	@pipenv run gunicorn --worker-class gevent --log-file - trood_task.wsgi

locust:
	@pipenv run locust -f tests/locustfile.py -H $(TESTHOST)

check:
	@curl -X GET $(TESTHOST)/v1/activity/ -H "accept: application/json" | json_pp

test:
	@pipenv run pytest

realtest:
	@pipenv run pytest -m 'realtest'

.PHONY: default locust run test realtest check
