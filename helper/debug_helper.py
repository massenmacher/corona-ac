from flask import current_app as app, flash


def flash_on_dev(message, category="message"):
    if app.config["ENV"] == "development":
        flash(message, category)
