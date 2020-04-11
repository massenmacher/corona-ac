from flask import Flask, request, render_template
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import pandas as pd

from models.Base import Base
from models.CaseDataEntry import CaseDataEntry

CONFIG = {
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///data/corona_ac.sqlite'
}

app = Flask(__name__)

# Init SQLAlchemy
engine = create_engine(CONFIG['SQLALCHEMY_DATABASE_URI'], connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


@app.route('/cases')
def cases():
    query = session.query(CaseDataEntry)
    case_data_entries = query.order_by(asc(CaseDataEntry.timestamp)).all()
    columns = [col.name for col in case_data_entries[0].__table__.columns]
    print(columns)

    return render_template("CaseDataEntry/index.html", entries=case_data_entries, columns=columns)


@app.route('/cases/add/csv', methods=['GET', 'POST'])
def add_csv():
    if request.method == 'GET':
        return render_template('CaseDataEntry/add_csv.html')
    else:
        if request.files and request.files['file']:
            # TODO: rather unsafe. Never trust user input
            file_contents = request.files['file']
            df = pd.read_csv(
                file_contents,
                delimiter=';',
                parse_dates=["Date"],
                dayfirst=True,
            )

            try:
                entries = []
                for index, row in df.iterrows():
                    entry = CaseDataEntry(
                        cases_region=row["Cases (Region)"],
                        cases_city=row["Cases (City)"],
                        deaths=row["Deaths"],
                        recovered=row["Recovered"],
                        timestamp=row["Date"]
                    )
                    entries.append(entry)

                session.add_all(entries)
                session.commit()
                return "Success", 201

            except Exception as e:
                raise e
                return f"Could not add. BC: {e}", 500

        return str(request.files)


@app.route('/cases/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        if request.form:
            try:
                entry = CaseDataEntry(
                    cases_region=request.form["cases_reg"],
                    cases_city=request.form["cases_city"],
                    deaths=request.form["deceased"],
                    recovered=request.form["recovered"],
                    timestamp=datetime.fromisoformat(f"{request.form['date']}T{request.form['time']}")
                )
                session.add(entry)
                session.commit()
                return "Added", 201

            except Exception as e:
                return f"Failed due to {e}", 500

        return "Failed. No Form data.", 400
    else:
        #return str(CaseDataEntry.metadata)
        return render_template("CaseDataEntry/add.html", form_fields=CaseDataEntry.metadata, now=datetime.now())

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    app.run()
