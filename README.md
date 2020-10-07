# Corona Statistics for Aachen, Germany
This small app is to give some small information and statistics about the development of the Corona Virus (a.k.a. COVID-19) in the _Städteregion Aachen_ and City of _Aachen_, Germany.

---
## Install
### Requirements
This project requires the following things:

- Python
    - pip
    - virtualenv
- possibly a C/C++ compiler (especially for Windows)

### Installation
**1) Create a VENV**

We recommend to use a virtual environment to avoid conflicts with other apps/software and to have it capsulated. This has the added benefit that you can easily clean up when you don't want to use the software anymore.

Just run the following command to create a suiting virual environment:
```
virtualenv venv
```

**2) Activate the virtual env**
To activate it, type:

- Linux-like systems: `source venv/bin/activate` or 
- Windows: `venv\Scripts\activate` (Use CMD -- Powershell may cause problems)


**3) Install the requirements**
We have compiled a requirements file, so that you can easily download all necessary files.

Install the required python packages by typing the following in the virtual env:

    pip intall --upgrade -r requirements.txt

(on linux systems you may need to use `pip3` instead of `pip`)

**4) Download the JS/CSS packages for statics**
As we do not want to bundle bootstrap and chart.js (this just clutters the repo) you need to optain these files seperately.

This can be done here:
- [Chart.JS](https://github.com/chartjs/Chart.js/releases)
- [Bootstrap](https://getbootstrap.com/docs/4.5/getting-started/download/)
- [moment.js](https://momentjs.com/downloads/moment.js)
- [jquery](https://jquery.com/download/)

Estract the minified files* in the corresponding `static/css` or `static/js` folders.

**5) Initialize the database and run migrations**
Run the migrations so that you always have the latest and correct database:

    flask db upgrade

**6) Edit the app config**
To properly configure the application, you need to create a configuration file called `app_config.py` in the `/config` folder.

You can use the provided sample config as a starting point.

**Please Note:** you need to create an app secret. You can create one by issuing the following command on yor machine as suggested by the official Flask docs [1]:

    python -c "import os; print(os.urandom(16))"

[1]: [Flask Documentation#Seessions](https://flask.palletsprojects.com/en/1.1.x/quickstart/#sessions)

**7) Start the app**

You should now be able to get going.

To start the app for local development, run `flask run` or `python app.py` (on linux systems you often need to use `python3` instead of `python`).

**Notice:** for productive environments we recommend to use a proper deployment and web server solution to mitigate possible risks and for better controlability and performance. 

---
## Upgrades
If you have an already running version and want to upgrade to the latest version, there might be some migrations needed. 

To run the migrations done through the `alembic` interface of `Flask-Migrate` just run 

    alembic upgrade head

to get to the newest schema.
