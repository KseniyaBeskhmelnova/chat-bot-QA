run:
	python -m bot

install:
	pip install -r requirements.txt

build:
	docker build -t echo-bot .

run-docker:
	docker run --env-file .env echo-bot