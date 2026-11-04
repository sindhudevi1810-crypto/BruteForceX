from flask import (
    Flask, render_template, request,
    redirect, url_for, flash, session
)

from database import initialize_database, create_demo_users
from auth import authenticate_user

app = Flask(__name__)
app.secret_key = "bruteforcex-local-development-key"

# Initialize the local demonstration database
initialize_database()
create_demo_users()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        success, message = authenticate_user(username, password)

        if success:
            session["username"] = username
            flash(message, "success")
            return redirect(url_for("dashboard"))

        flash(message, "error")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        username=session["username"]
    )


# Automatic dictionary attack simulation
@app.route("/simulate", methods=["GET", "POST"])
def simulate():
    results = []

    if request.method == "POST":
        target = request.form.get("target")

        if target not in ("weak_user", "secure_user"):
            flash("Invalid demo account selected.", "error")
        else:
            candidates = [
                "password",
                "123456",
                "admin123",
                "welcome",
                "cat123",
                "student123",
                "StrongDemo@123"
            ]

            for attempt, guess in enumerate(candidates, start=1):
                success, message = authenticate_user(target, guess)

                results.append({
                    "attempt": attempt,
                    "message": message,
                    "success": success
                })

                if success or "locked" in message.lower():
                    break

    return render_template("results.html", results=results)


# NEW: Manual password testing against local demo accounts
@app.route("/manual-test", methods=["GET", "POST"])
def manual_test():
    result = None

    if request.method == "POST":
        target = request.form.get("target", "")
        password = request.form.get("password", "")

        if target not in ("weak_user", "secure_user"):
            result = "Please select a valid demo account."
        elif not password:
            result = "Please enter a password."
        else:
            success, message = authenticate_user(target, password)
            result = message

    return render_template("manual_test.html", result=result)


# NEW: Password strength checker
def check_password_strength(password):
    checks = {
        "At least 8 characters": len(password) >= 8,
        "Contains uppercase letter": any(c.isupper() for c in password),
        "Contains lowercase letter": any(c.islower() for c in password),
        "Contains a number": any(c.isdigit() for c in password),
        "Contains special character": any(
            not c.isalnum() for c in password
        )
    }

    score = sum(checks.values())

    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    return strength, checks


@app.route("/password-strength", methods=["GET", "POST"])
def password_strength():
    strength = None
    checks = None

    if request.method == "POST":
        password = request.form.get("password", "")
        strength, checks = check_password_strength(password)

    return render_template(
        "password_strength.html",
        strength=strength,
        checks=checks
    )


# NEW: Vulnerable vs protected comparison
@app.route("/comparison")
def comparison():
    return render_template("comparison.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)