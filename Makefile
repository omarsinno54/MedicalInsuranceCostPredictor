install:
	pip install -r requirements.txt

format:
	black .

app:
	python app.py

mlflow:
	mlflow server --host 127.0.0.1 --port 5000