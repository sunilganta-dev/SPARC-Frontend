from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import requests

applicant_public_bp = Blueprint("applicant_public", __name__, template_folder="../templates")

# ---------------------------------------------------------
# Route: Public applicant form with optional preselected matchmaker
# ---------------------------------------------------------
@applicant_public_bp.route("/", methods=["GET", "POST"])
@applicant_public_bp.route("/<int:matchmaker_id>", methods=["GET", "POST"])
def apply(matchmaker_id=None):
    # ✅ Fetch all matchmakers from backend
    matchmakers = []
    try:
        response = requests.get(f"{current_app.config['API_URL']}/matchmaker")
        if response.status_code == 200:
            matchmakers = response.json()
    except Exception as e:
        flash(f"Error fetching matchmakers: {e}", "danger")

    if request.method == "POST":
        # Collect form data
        data = {
            "first_name": request.form.get("first_name"),
            "last_name": request.form.get("last_name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "dob": request.form.get("dob"),
            "gender": request.form.get("gender"),
            "city": request.form.get("city"),
            "state": request.form.get("state"),
            "country": request.form.get("country"),
            "religious_level": request.form.get("religious_level"),
            "kosher_level": request.form.get("kosher_level"),
            "shabbat_observance": request.form.get("shabbat_observance"),
        }

        # Matchmaker comes either from dropdown or preselected route
        chosen_matchmaker = request.form.get("matchmaker_id") or matchmaker_id

        # Handle file upload
        file = request.files.get("picture")
        files = {}
        if file and file.filename != "":
            files = {"picture": (file.filename, file.stream, file.mimetype)}

        try:
            # Send data to backend API
            api_url = f"{current_app.config['API_URL']}/applicants/apply/{chosen_matchmaker}"
            response = requests.post(api_url, data=data, files=files)

            if response.status_code == 201:
                flash("Application submitted successfully!", "success")
                return redirect(url_for("index"))
            else:
                flash(f"Failed to submit: {response.json().get('error', 'Unknown error')}", "danger")

        except Exception as e:
            flash(f"Error connecting to API: {e}", "danger")

    return render_template(
        "applicants/public_apply.html",
        matchmakers=matchmakers,
        selected_matchmaker_id=matchmaker_id
    )
