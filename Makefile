all:
	@echo "make lint	- Check code with flake8"
	@echo "make test	- Run tests"
	@echo "make local	- Run app locally"
	@echo "make docker	- Run app and db docker containers"
	@exit 0

lint:
	flake8 app --count --exit-zero --exclude=app/db/migrations/ --max-complexity=10 --max-line-length=127 --statistics
	flake8 tests --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

test:
	pytest --disable-warnings

local:
	uvicorn app.main:app --reload

docker:
	docker-compose up -d --build
