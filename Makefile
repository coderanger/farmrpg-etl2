develop:
	python -m uvicorn --reload farmrpg_etl.asgi:application --port 8001

sdevelop:
	env SYNC_DEVELOP=1 python manage.py runserver

test:
	python -m pytest

ftest:
	python -m pytest --reuse-db --no-cov

psql:
	python manage.py dbshell

migrate:
	python manage.py migrate

watchci:
	gh run watch "$$(gh run list --json databaseId --jq ".[0].databaseId")"

deploy:
	kubectl delete pod --context farmrpg-etl --namespace etl --all
