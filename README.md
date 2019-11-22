# autobuses

## Deploy locally

```
$ # Install python dependencies
$ pip install -r requirements.txt
$ # Configure Flask entrypoint
$ export FLASK_APP=server.py
$ # In windows
C: set FLASK_APP=server.py
$ # Run flask dev server
$ flask run --port 5001
$ # Run flask dev server available outside of localhost
$ flask run --host 0.0.0.0 --port 5001
```

## Dependecies used

### MySQL

MySQL connection must be set up in the [secrets.json](secrets.json) file. The server used must have the [set up script](SQL/script.sql) run on it.

### Python

* flask: Web framework [Quickstart documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
* flask_cors: A Flask extension for handling Cross Origin Resource Sharing (CORS). [Documentation](https://flask-cors.readthedocs.io/en/latest/)
* requests: To send HTTP requests to retrieve API results [Documentation](https://2.python-requests.org/en/master/)
* mysql.connector: Allow connexions with MySQL databases. Used through the wrapper [DB.py](utils/DB.py). [Documentation](https://dev.mysql.com/doc/connector-python/en/)
* google-auth: Verification and decoding of OAuth token ids. It's client ID must be set up in the [secrets.json](secrets.json) file. [Documentation](https://developers.google.com/identity/sign-in/web/backend-auth)
* locust.io: Optional. Allows the execution of load testing. More information on usage at [load testing](#load-testing). [Documentation](https://docs.locust.io/en/stable/)

### External data sources

* Open Data Malaga: Open data repository, no apikey required. [Link](https://datosabiertos.malaga.eu/)

## Load testing
To run load testing:

```bash
$ locust -f load_testing.py --host=http://localhost:5001
```

After launching it go to [http://localhost:8089](http://localhost:8089) and set the number of concurrent users and spawn rate.
