# DOT Precipitation Dash Application 

## Structure

 * `application.py` contains the main app loop code.
 * `gui.py` has most user interface elements.
 * `data.py` has data fetch code.
 * `luts.py` has shared code & lookup tables and other configuration.
 * `assets/` has images and CSS (uses [Bulma](https://bulma.io))

## Local development

After cloning this template, run it this way:

```
pipenv install
export FLASK_APP=application.py
export FLASK_DEBUG=True
pipenv run flask run
```

The project is run through Flask and will be available at [http://localhost:5000](http://localhost:5000).  Setting `FLASK_DEBUG` to `True` will use a local file for source data (bypassing API calls) and enable other debugging tools by default.

Other env vars that can be set:

 * `DASH_LOG_LEVEL` - sets level of logger, default INFO
 * `API_URL` - Has default (http://apollo.snap.uaf.edu:3000/api/percentiles)

## Deploying to AWS Elastic Beanstalk:

```
eb init # only needed once!
pipenv run pip freeze > requirements.txt
eb deploy
```

The following env vars must be set:

 * `DASH_REQUESTS_PATHNAME_PREFIX` - URL fragment so requests are properly routed.

