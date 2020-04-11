from flask import Flask
import DB

from views.dashboard import dashboard
from views.CaseDataEntry import case_data

from models.Base import Base
from models.CaseDataEntry import CaseDataEntry

CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///data/corona_ac.sqlite'
}

app = Flask(__name__)
# Init SQLAlchemy
# engine = create_engine(CONFIG['SQLALCHEMY_DATABASE_URI'], connect_args={'check_same_thread': False})
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
# # Base.query = db_session.query_property()
DB.init_engine(CONFIG['SQLALCHEMY_DATABASE_URI'])
DB.init_session()


app.register_blueprint(dashboard)
app.register_blueprint(case_data)

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run()
