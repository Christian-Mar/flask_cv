from flask import render_template

from ...services.cv_service import get_cv, save_message
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

    save_message(form.name.data, form.email.data, form.subject.data, form.message.data)
    return "OK"
