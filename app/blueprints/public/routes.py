from datetime import datetime, timezone

from flask import render_template

from ...extensions import get_db
from ...services.cv_service import get_cv
from . import bp
from .forms import ContactForm


@bp.get("/")
def index():
    return render_template("public/index.html", cv=get_cv())


@bp.post("/contact")
def contact():
    form = ContactForm()
    if not form.validate_on_submit():
        errors = [e for errs in form.errors.values() for e in errs]
        return "; ".join(errors) or "Ongeldig formulier", 200

    get_db().messages.insert_one(
        {
            "name": form.name.data,
            "email": form.email.data,
            "subject": form.subject.data,
            "body": form.message.data,
            "created_at": datetime.now(timezone.utc),
            "read": False,
        }
    )
    return "OK"
