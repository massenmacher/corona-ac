from datetime import datetime
from flask import render_template, Blueprint, request
from sqlalchemy import asc
import pandas as pd

from DB import session
from models.CaseDataEntry import CaseDataEntry

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/")
def dashboard_home():
    return "Home"