import hashlib
import traceback

import requests
from app.decorators import login_required
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


@Login.route("/login", methods=["GET", "POST"])
def login():
    err = ""
    if request.method == "POST":
        try:
            laData = request.form.to_dict()
            if laData["CNRODNI"] is None or len(laData["CNRODNI"]) != 8:
                raise ValueError("ERROR EN NRO DE DOCUMENTO")
            elif laData["CCLAVE"] is None:
                raise ValueError("CLAVE NO DEFINIDA")
            clave = hashlib.sha512(laData["CCLAVE"].encode("utf-8"))
            laData["CCLAVE"] = clave.hexdigest()
            laData["CDIRIP"] = request.remote_addr
            laData["NIDAPP"] = 2
            loJson = json.dumps(laData)
            llOk = requests.post(
                current_app.config["API_URL"] + "/login", json=loJson
            ).json()
            if not llOk["OK"]:
                raise ValueError(llOk["DATA"])
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


@Login.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("Login.login"))


@Login.route("/user", methods=["GET"])
def user():
    return render_template("login.html", title="login", error="")


@Login.route("/main", methods=["GET"])
@login_required
def main():
    lcCodUsu = session["CCODUSU"]
    err = ""
    ploads = {"CCODUSU": lcCodUsu}
    try:
        llOk = requests.get(
            current_app.config["API_URL"] + "/main", params=ploads
        ).json()
        if not llOk["OK"]:
            raise ValueError(llOk["DATA"])
        laDatos = llOk["DATA"]
        session["ROUTES"] = laDatos
        return render_template("main.html", title="main", error=err, saDatos=laDatos)
    except Exception as e:
        traceback.print_exc()
        err = str(err)
        flash(err, "error")
        return redirect(url_for("Login.login"))
