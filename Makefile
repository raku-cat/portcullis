all: app

app:
	python3 -m venv ./python_modules
	./python_modules/pip install -r requirements.txt