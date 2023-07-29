all: app

app:
	python3 -m venv ./python_modules
	./python_modules/bin/pip install -r requirements.txt
