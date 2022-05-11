python -m src.download_models
gunicorn --chdir src server:app -w 2 --threads 2 -b 0.0.0.0:8000
