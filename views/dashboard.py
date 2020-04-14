from flask import render_template, Blueprint, flash
from sqlalchemy import asc

from DB import db_session
from models.CaseDataEntry import CaseDataEntry

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
def dashboard_home():
    query = db_session.query(CaseDataEntry)
    case_data_entries = query.order_by(asc(CaseDataEntry.timestamp)).all()
    columns = [col.name for col in case_data_entries[0].__table__.columns]

    return render_template("Dashboard/dashboard.html", entries=case_data_entries, columns=columns)