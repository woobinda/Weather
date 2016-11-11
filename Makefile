start:
	pip install -r requirements.txt
	gunicorn run:app
