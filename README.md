# autobuses

## Deploy locally

```
$ # Install python dependencies
$ pip install -r requirements.txt
$ # Configure Flask entrypoint
$ export FLASK_APP=app/app/main.py
$ # Run flask dev server
$ flask run
```

## Load testing
To run load testing:

```bash
$ locust -f load_testing.py --host=http://localhost:5000
```