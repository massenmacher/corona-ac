from datetime import datetime
from flask import render_template, Blueprint, request, url_for, flash, redirect
from sqlalchemy import asc
import pandas as pd

from models.Base import db
from helper.debug_helper import flash_on_dev
from helper.page_parser import fetch_and_parse_page_data, parse_data
from models.CaseDataEntry import CaseDataEntry

case_data = Blueprint("case_data", __name__)
db_session = db.session

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
                        timestamp=row["Date"],
                        alsdorf=row["Alsdorf"],
                        baesweiler=row["Baesweiler"],
                        eschweiler=row["Eschweiler"],
                        herzogenrath=row["Herzogenrath"],
                        monschau=row["Monschau"],
                        roetgen=row["Roetgen"],
                        simmerath=row["Simmerath"],
                        stolberg=row["Stolberg"],
                        wuerselen=row["Wuerselen"]
                    )
                    entries.append(entry)

                db_session.add_all(entries)
                db_session.commit()

                flash("Success", "success")
                return render_template("simple_text.html", html="Import successfull."), 201

            except Exception as e:
                message = f"Data import was not successful. Something went wrong. Please try again."
                flash(message, "error")
                flash_on_dev(e, "error")
                return render_template("simple_text.html", text=message), 500

        flash("Oooops. There went something wrong. Please try again.", 500)
        return redirect("case_data.add_csv"), 500


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
                    timestamp=datetime.fromisoformat(f"{request.form['date']}T{request.form['time']}"),
                    alsdorf=request.form["alsdorf"],
                    baesweiler=request.form["baesweiler"],
                    eschweiler=request.form["eschweiler"],
                    herzogenrath=request.form["herzogenrath"],
                    monschau=request.form["monschau"],
                    roetgen=request.form["roetgen"],
                    simmerath=request.form["simmerath"],
                    stolberg=request.form["stolberg"],
                    wuerselen=request.form["wuerselen"]
                )
                session = db_session()
                session.add(entry)
                session.commit()

                flash("Data successfully added.")

                return render_template("simple_text.html", text=f"Data entry successfully added."), 201

            except Exception as e:
                flash("An error occurred!", "error")
                flash_on_dev(e, "error")

                return render_template("simple_text.html", text=f"Could not add entry. Please try again!",
                                       back_to=(url_for("case_data.add"), "Back to data entry")), 500

        flash("Error. You did not enter any or invalid data. Please try again.", "error")
        return redirect('case_data.add'), 400
    else:
        return render_template("CaseDataEntry/add.html", form_fields=CaseDataEntry.metadata, now=datetime.now())


@case_data.route("/cases/fetch")
def fetch_from_page():
    results = fetch_and_parse_page_data()

    if results is None or len(results) == 0:
        flash("No data received")
        return render_template("simple_text.html", text="No data found")

    return render_template("CaseDataEntry/add_from_external_page.html", data=results)

@case_data.route("/cases/text", methods=["GET", "POST"])
def fetch_via_text():
    if request.method == "GET":
        return render_template("CaseDataEntry/add_via_text.html")

    else:
        if request.form:
            try:
                date_text, content_text = request.form["text"].split("\n", maxsplit=1)
                
                result = parse_data(date_text, content_text)
                print(result)

                flash("Data successfully added.")

                return render_template("CaseDataEntry/add_from_external_page.html", data=[result])

            except Exception as e:
                flash("An error occurred!", "error")
                flash_on_dev(e, "error")

                return render_template("simple_text.html", text=f"Could not add entry. Please try again!",
                                       back_to=(url_for("case_data.add"), "Back to data entry")), 500

