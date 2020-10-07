from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from views.dashboard import dashboard
from views.CaseDataEntry import case_data

from models.Base import db
from models.CaseDataEntry import CaseDataEntry

app = Flask(__name__)
app.config.from_pyfile('config/example_config.py')
app.config.from_pyfile('config/app_config.py')

db.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(dashboard)
app.register_blueprint(case_data)

if __name__ == '__main__':
    app.run()
