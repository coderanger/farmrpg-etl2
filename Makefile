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

watchci:
	gh run watch "$$(gh run list --json databaseId --jq ".[0].databaseId")"

deploy:
	kubectl delete pod --context farmrpg-etl --namespace etl --all
