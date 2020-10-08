from flask import render_template, Blueprint, flash
from sqlalchemy import asc
import pandas as pd

from models.Base import db
from models.CaseDataEntry import CaseDataEntry

dashboard = Blueprint("dashboard", __name__)
db_session = db.session

@dashboard.route("/")
def dashboard_home():
    query = db_session.query(CaseDataEntry)
    case_data_entries = query.order_by(asc(CaseDataEntry.timestamp)).all()
    if len(case_data_entries) > 0:
        columns = [col.name for col in case_data_entries[0].__table__.columns]
    else:
        columns = []

    return render_template("Dashboard/dashboard.html", entries=case_data_entries, columns=columns)


@dashboard.route("/active")
def dashboard_active():
    query = db_session.query(CaseDataEntry)
    case_data_entries = query.order_by(asc(CaseDataEntry.timestamp)).all()

    timestmp = list(map(lambda e: e.timestamp, case_data_entries))
    infected = list(map(lambda e: e.cases_region, case_data_entries))
    deceased = list(map(lambda e: e.deaths, case_data_entries))
    recoverd = list(map(lambda e: e.recovered, case_data_entries))

    active_cases = []
    for i in range(len(case_data_entries)):
        active = infected[i] - (recoverd[i] or 0) - (deceased[i])
        active_cases.append((active, timestmp[i]))


    return render_template("Dashboard/aspect_graph.html", entries=active_cases, label="Active Cases")


@dashboard.route("/newcases")
def dashboard_newcases():
    query = db_session.query(CaseDataEntry)
    case_data_entries = query.order_by(asc(CaseDataEntry.timestamp)).all()

    timestmp = list(map(lambda e: e.timestamp, case_data_entries))
    infected = list(map(lambda e: e.cases_region, case_data_entries))
    
    infected.insert(0,0)

    new_cases = []
    for i in range(len(case_data_entries)):
        diff = infected[i+1] - infected[i]
        new_cases.append((diff, timestmp[i])) 

    return render_template("Dashboard/aspect_graph.html", entries=new_cases, label="New Cases")

@dashboard.route("/newcases/day")
def dashboard_newcases_meanday():
    query = db_session.query(CaseDataEntry)
    case_data_entries = query.order_by(asc(CaseDataEntry.timestamp)).all()

    timestmp = list(map(lambda e: e.timestamp, case_data_entries))
    infected = list(map(lambda e: e.cases_region, case_data_entries))
    
    infected.insert(0,0)

    new_cases = []
    for i in range(2, len(case_data_entries)):
        diff = infected[i+1] - infected[i]
        timedelta = (timestmp[i]-timestmp[i-1])
        diff /= (timedelta.total_seconds() / (60*60*24))
        new_cases.append((diff, timestmp[i])) 

    return render_template("Dashboard/aspect_graph.html", entries=new_cases, label="New Cases")

@dashboard.route("/incidence")
def dashboard_incidence():
    CITIZENS = 557026 # For Aachen city: 258816

    query = db_session.query(CaseDataEntry)

    df = pd.read_sql_query(query.order_by(asc(CaseDataEntry.timestamp)).statement, db_session.bind)

    df_diff = df.set_index("timestamp").sort_index(ascending=True).diff()

    df_week_diff = df_diff.resample("1W")["cases_region"].sum()
    
    df_incidence = df_week_diff / (CITIZENS/100000)

    #print(df_incidence)

    incidences = [(value, index) for index, value in df_incidence.iteritems()]

    return render_template("Dashboard/aspect_graph.html", entries=incidences, label="7 Day Incidence")
