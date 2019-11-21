# autobuses

## Deploy locally

```
$ # Install python dependencies
$ pip install -r requirements.txt
$ # Configure Flask entrypoint
$ export FLASK_APP=main.py
$ # In windows
C: set FLASK_APP=main.py
$ # Run flask dev server
$ flask run
$ # Run flask dev server available outside of localhost
$ flask run --host 0.0.0.0
```

## Dependecies used

### MySQL

MySQL connection must be set up in the [database.config](database.config) file.

### Python

* flask: Web framework [Quickstart documentation](https://flask.palletsprojects.com/en/1.1.x/quickstart/)
* requests: To send HTTP requests to retrieve API results [Documentation](https://2.python-requests.org/en/master/)
* mysql.connector: Allow connexions with MySQL databases. Used through the wrapper [DB.py](utils/DB.py). [Documentation](https://dev.mysql.com/doc/connector-python/en/)
* locust.io: Optional. Allows the execution of load testing. More information on usage at [load testing](#load-testing). [Documentation](https://docs.locust.io/en/stable/)

### Javascript

* leafletjs: Open source library for interactive mobile friendly maps. [Documentation](https://leafletjs.com/reference-1.6.0.html)
* Google OAuth 2.0: Google sign-in integration [Documentation](https://developers.google.com/identity/sign-in/web/sign-in)
* Fontawesome: Open source icon set [Documentation](https://fontawesome.com/how-to-use/on-the-web/referencing-icons/basic-use)

### External data sources

* Open Data Malaga: Open data repository, no apikey required. [Link](https://datosabiertos.malaga.eu/)
* Dark Sky API: Weather forecasting API with free tier. It's apikey must be set up in the [secrets.json](secrets.json) file. [Documentation](https://darksky.net/dev/docs)

## Load testing
To run load testing:

```bash
$ locust -f load_testing.py --host=http://localhost:5000
```

After launching it go to [http://localhost:8089](http://localhost:8089) and set the number of concurrent users and spawn rate.
