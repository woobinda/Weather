install:
	pip install -r requirements.txt

start:
	gunicorn run:app
