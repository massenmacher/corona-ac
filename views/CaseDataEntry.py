from datetime import datetime
from flask import render_template, Blueprint, request, url_for
from sqlalchemy import asc
import pandas as pd

from DB import db_session, session
from models.CaseDataEntry import CaseDataEntry

case_data = Blueprint("case_data", __name__)


@case_data.route('/cases')
def cases():
    query = db_session.query(CaseDataEntry)
    case_data_entries = query.order_by(asc(CaseDataEntry.timestamp)).all()
    columns = [col.name for col in case_data_entries[0].__table__.columns]

    return render_template("CaseDataEntry/index.html", entries=case_data_entries, columns=columns)


@case_data.route('/cases/add/csv', methods=['GET', 'POST'])
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

                db_session.add_all(entries)
                db_session.commit()
                return "Success", 201

            except Exception as e:
                raise e
                return f"Could not add. BC: {e}", 500

        return str(request.files) #TODO: Edit this


@case_data.route('/cases/add', methods=['GET', 'POST'])
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
                session = db_session()
                session.add(entry)
                session.commit()
                return render_template("simple_text.html", html=f"Added<br><a class='btn btn-info' href={url_for('dashboard.dashboard_home')}>Back to Dashboard</a>"), 201

            except Exception as e:
                return render_template("simple_text.html", html=f"Failed due to {e}"), 500

        return render_template("simple_text.html", html="Failed. No Form data."), 400
    else:
        return render_template("CaseDataEntry/add.html", form_fields=CaseDataEntry.metadata, now=datetime.now())
