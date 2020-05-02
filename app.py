from flask import Flask
import DB

from views.dashboard import dashboard
from views.CaseDataEntry import case_data

from models.Base import Base
from models.CaseDataEntry import CaseDataEntry

app = Flask(__name__)
app.config.from_pyfile('config/example_config.py')
app.config.from_pyfile('config/app_config.py')
print(app.config)

# Init SQLAlchemy
engine = DB.init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.create_all(engine)
session = DB.init_session()


app.register_blueprint(dashboard)
app.register_blueprint(case_data)

if __name__ == '__main__':
    app.run()
