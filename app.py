from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = "jalajala-secret-key-2025"


# ─── Demo Accounts ────────────────────────────────────────
USERS = {
    "sa_reyes01": {
        "password": "Adm!nSecure91",
        "full_name": "Andre Miguel Reyes",
        "role": "Super Admin",
        "email": "andre.reyes@tourismsys.com",
        "status": "Active",
    },
    "sa_mendoza02": {
        "password": "Sup3rCtrl88",
        "full_name": "Karla Denise Mendoza",
        "role": "Super Admin",
        "email": "karla.mendoza@tourismsys.com",
        "status": "Active",
    },
    "sa_navales03": {
        "password": "RootAccess77",
        "full_name": "Jonav Pierre Navales",
        "role": "Super Admin",
        "email": "jonav.navales@tourismsys.com",
        "status": "Inactive",
    },
    "admin_cruz01": {
        "password": "T0ur1smAdm23",
        "full_name": "Maria Isabel Cruz",
        "role": "Admin",
        "email": "maria.cruz@jalajala.gov.ph",
        "status": "Active",
    },
    "admin_garcia02": {
        "password": "Dashb0ard55",
        "full_name": "Paolo Enrique Garcia",
        "role": "Admin",
        "email": "paolo.garcia@jalajala.gov.ph",
        "status": "Active",
    },
    "admin_santos03": {
        "password": "Upd8List!21",
        "full_name": "Leah Andrea Santos",
        "role": "Admin",
        "email": "leah.santos@jalajala.gov.ph",
        "status": "Inactive",
    },
    "user_calim01": {
        "password": "JennyTrip22",
        "full_name": "Jenny Mae Calim",
        "role": "Citizen/User",
        "email": "jenny.calim@email.com",
        "status": "Active",
    },
    "user_lopez02": {
        "password": "TravelGuy90",
        "full_name": "Mark Anthony Lopez",
        "role": "Citizen/User",
        "email": "mark.lopez@email.com",
        "status": "Active",
    },
    "user_ramirez03": {
        "password": "Lakbay2020",
        "full_name": "Angela Marie Ramirez",
        "role": "Citizen/User",
        "email": "angela.ramirez@email.com",
        "status": "Inactive",
    },
}


# ─── Helper: require login ─────────────────────────────────
def get_current_user():
    username = session.get("username")
    if username and username in USERS:
        return {"username": username, **USERS[username]}
    return None


# ─── Login ────────────────────────────────────────────────
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        user = USERS.get(username)

        if not user:
            error = "Username not found."
        elif user["password"] != password:
            error = "Incorrect password."
        elif user["status"] == "Inactive":
            error = "This account is inactive. Please contact the administrator."
        else:
            session["username"] = username
            return redirect(url_for("dashboard"))

    return render_template("login.html", error=error)


# ─── Logout ───────────────────────────────────────────────
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ─── Dashboard ────────────────────────────────────────────
@app.route("/dashboard")
def dashboard():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template(
        "dashboard.html",
        page_title="Dashboard",
        active_page="dashboard",
        current_user=user,
    )


# ─── Users ────────────────────────────────────────────────
@app.route("/users")
def users():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    user_list = [
        {"id": i + 1, "username": u, **USERS[u]}
        for i, u in enumerate(USERS)
    ]
    return render_template(
        "users.html",
        page_title="User Management",
        active_page="users",
        current_user=user,
        user_list=user_list,
    )


# ─── Tourist Destinations ─────────────────────────────────
@app.route("/tourist-destinations")
def tourist_destinations():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template(
        "tourist_destinations.html",
        page_title="Tourist Destinations",
        active_page="tourist_destinations",
        current_user=user,
    )


# ─── Resorts ──────────────────────────────────────────────
@app.route("/resorts")
def resorts():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template(
        "resorts.html",
        page_title="Resorts",
        active_page="resorts",
        current_user=user,
    )


# ─── Bookings ─────────────────────────────────────────────
@app.route("/bookings")
def bookings():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template(
        "bookings.html",
        page_title="Bookings",
        active_page="bookings",
        current_user=user,
    )


# ─── Run ──────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
