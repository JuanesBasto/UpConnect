from flask import Blueprint, render_template, session, redirect, url_for, flash

main_bp = Blueprint('main', __name__)

@main_bp.route("/dashboard")
def dashboard():
    if "user_id" in session:
        return render_template("dashboard.html")
    else:
        flash("Debes iniciar sesión primero", "warning")
        return redirect(url_for("auth.login"))
