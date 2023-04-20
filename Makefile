develop:
	python -m uvicorn --reload etl.asgi:application

sdevelop:
	env SYNC_DEVELOP=1 python manage.py runserver

test:
	python -m pytest

ftest:
	python -m pytest --reuse-db --no-cov

psql:
	python manage.py dbshell
