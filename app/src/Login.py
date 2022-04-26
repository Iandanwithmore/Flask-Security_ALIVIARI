import hashlib
import traceback

import requests
from app.decorators import login_required, exception_handler
from flask import (
    Blueprint,
    current_app,
    flash,
    json,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

Login = Blueprint("Login", __name__)

@Login.get("/login")
@Login.post("/login")
@exception_handler("Login.login")
def login():
    err = ""
    if request.method == "POST":
        try:
            laData = request.form.to_dict()
            assert(laData["CNRODNI"] is None or len(laData["CNRODNI"]) != 8),"ERROR EN NRO DE DOCUMENTO"
            assert laData["CCLAVE"] is None, "CLAVE NO DEFINIDA"
            clave = hashlib.sha512(laData["CCLAVE"].encode("utf-8"))
            laData["CCLAVE"] = clave.hexdigest()
            laData["CDIRIP"] = request.remote_addr
            laData["NIDAPP"] = 2
            loJson = json.dumps(laData)
            llOk = requests.post(
                current_app.config["API_URL"] + "/login", json=loJson
            ).json()
            assert not llOk["OK"],llOk["DATA"]
            laData = llOk["DATA"]
            session["CCODUSU"] = laData["CCODUSU"]
            session["CNOMBRE"] = laData["CNOMBRE"]
            session["CCARGO"] = laData["CCARGO"]
            session["TMP"] = None
            session["paData"] = None
            session["paDatos"] = None
            flash("Login OK!", "success")
            return redirect(url_for("Login.main"))
        except Exception as e:
            traceback.print_exc()
            err = str(err)
            flash(err, "error")

    return render_template("login.html", title="login", error=err)

@Login.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("Login.login"))

@Login.get("/user")
def user():
    return render_template("login.html", title="login", error="")

@Login.get("/main")
@login_required
@exception_handler("Login.login")
def main():
    err = ""
    ploads = {"CCODUSU": session["CCODUSU"]}
    llOk = requests.get(
        current_app.config["API_URL"] + "/main", params=ploads
    ).json()
    assert not llOk["OK"],llOk["DATA"]
    laDatos = llOk["DATA"]
    session["ROUTES"] = laDatos
    return render_template("main.html", title="main", error=err, saDatos=laDatos)