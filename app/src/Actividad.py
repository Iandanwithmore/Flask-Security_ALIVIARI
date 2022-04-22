import asyncio
import traceback
from datetime import datetime
from itertools import groupby
from pathlib import Path

import requests
from app.CBase import CBase
from app.decorators import login_required, val_session_routes_factory
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    json,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

Actividad = Blueprint("Actividad", __name__)


def get_or_create_eventloop():
    try:
        return asyncio.get_event_loop()
    except RuntimeError as ex:
        if "There is no current event loop in thread" in str(
            ex
        ) or "Event loop is closed" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return asyncio.get_event_loop()


def fetch_async(urls):
    """Fetch list of web pages asynchronously."""
    loop = get_or_create_eventloop()  # event loop
    future = asyncio.ensure_future(fetch_all(urls, loop))  # tasks to do
    done = loop.run_until_complete(future)  # loop until done
    # loop.close()
    return done


async def fetch_all(urls, loop):
    tasks = []  # dictionary of start times for each url
    for url in urls:
        task = loop.run_in_executor(None, requests.get, url)
        tasks.append(task)  # create list of tasks
    done = await asyncio.gather(*tasks)  # gather task responses
    # done = asyncio.wait(*tasks)
    return done


@Actividad.route("/act_lab", methods=["GET"])
@Actividad.route("/act_ray", methods=["GET"])
@Actividad.route("/act_med", methods=["GET"])
@Actividad.route("/act_tri", methods=["GET"])
@Actividad.route("/act_car", methods=["GET"])
@Actividad.route("/act_aud", methods=["GET"])
@Actividad.route("/act_esp", methods=["GET"])
@Actividad.route("/act_oft", methods=["GET"])
@Actividad.route("/act_psi", methods=["GET"])
@Actividad.route("/act_eco", methods=["GET"])
@Actividad.route("/act_nut", methods=["GET"])
@Actividad.route("/act_odo", methods=["GET"])
def route_act():
    laservice = {
        "/act_lab": "L",
        "/act_ray": "R",
        "/act_med": "M",
        "/act_tri": "T",
        "/act_car": "C",
        "/act_aud": "A",
        "/act_esp": "E",
        "/act_oft": "O",
        "/act_psi": "P",
        "/act_eco": "G",
        "/act_nut": "N",
        "/act_odo": "D",
    }
    lcTipSer = "X"
    if request.path in laservice:
        lcTipSer = laservice[request.path]
    return redirect(url_for("Actividad.actividades", pcTipSer=lcTipSer))


@Actividad.route("/actividades/<string:pcTipSer>", methods=["GET"])
@val_session_routes_factory
@login_required
def actividades(pcTipSer):
    lcCodUsu = session["CCODUSU"]
    err = ""
    ploads = {"CTIPSER": pcTipSer, "CCODUSU": lcCodUsu}
    try:
        format = "%Y-%m-%d"
        if request.args.get("TINICIO") and request.args.get("TFIN"):
            ltInico = request.args["DINIACT"]
            ltFin = request.args["DFINACT"]
            datetime.strptime(ltInico, format)
            datetime.strptime(ltFin, format)
            ploads.append(
                {"DINIACT": request.args["DFINACT"], "TFINACT": request.args["TFIN"]}
            )
        else:
            now = datetime.now()
            date = now.strftime(format)
            laData = {"DINIACT": date, "DFINACT": date}
        llOk = requests.get(
            current_app.config["API_URL"] + "/view/actividades", params=ploads
        ).json()
        if llOk["OK"]:
            session["paDatos"] = llOk["DATA"]
        return render_template(
            "actividades.html",
            title="actividades",
            saData=laData,
            saDatos=session["paDatos"],
        )
    except Exception as e:
        traceback.print_exc()
        err = str(err)
        flash(err, "error")
        return redirect(url_for("Login.main"))


@Actividad.route(
    "/actividades/<string:pcTipSer>/<int:pnIndice>", methods=["GET", "POST"]
)
# @login_required
def detalleActividad(pcTipSer, pnIndice):
    lcCodUsu = session["CCODUSU"]
    err = ""
    try:
        if request.method == "GET":
            session["paCie10"] = None
            session["paIndicador"] = None
            if session.get("paDatos") is None:
                raise ValueError("DATOS SIN DEFINIR")
            session["paData"] = session["paDatos"][pnIndice]
            if session.get("paData") is None:
                raise ValueError("DATA SIN DEFINIR")
            ploads = [
                "CCODACT",
                "CTIPSER",
                "CCODPLA",
                "CNRODNI",
                "CNRORUC",
                "CCODUSU",
            ]
            for item in ploads:
                if session["paData"].get(item) is None:
                    raise ValueError(f"VARIABLE NO DEFINIDA : '{item}'")
            lcCodAct = session["paData"]["CCODACT"]
            urls = [
                current_app.config["API_URL"]
                + f"/actividad/detalle?CCODACT={lcCodAct}&CCODUSU={lcCodUsu}",
                current_app.config["API_URL"]
                + f"/actividad/cie10?CCODACT={lcCodAct}&CCODUSU={lcCodUsu}",
                current_app.config["API_URL"]
                + f"/actividad/extra?CCODACT={lcCodAct}&CCODUSU={lcCodUsu}",
            ]
            s = requests.Session()
            R0 = []
            for url in urls:
                r = s.get(url)
                R0.append(r.json())
            if not R0[0]["OK"]:
                raise ValueError("NO SE CARGO DETALLE DE LA ACTIVIDAD")
            if R0[1]["OK"]:
                session["paCie10"] = R0[1]["DATA"]
            if not R0[2]["OK"]:
                R3_json["DATA"] = []
            session["paIndicador"] = None if R0[0]["DATA"] is None else R0[0]["DATA"]
            res = [
                list(v)
                for k, v in groupby(session["paIndicador"], key=lambda x: x["NORDEN"])
            ]
            return render_template(
                "detalleActividad.html",
                title="Actividad detalle",
                saData=session["paData"],
                saCie10=session["paCie10"],
                saExtra=R0[2]["DATA"],
                saDatos=res,
            )
        elif request.method == "POST":
            ltAtenci = request.form["TATENCI"] if request.form.get("TATENCI") else ""
            lmObserv = request.form["COBSERV"] if request.form.get("COBSERV") else ""
            lmConclu = request.form["CCONCLU"] if request.form.get("CCONCLU") else ""
            lmRecome = request.form["CRECOME"] if request.form.get("CRECOME") else ""
            laDatos = []
            for laFila in session["paIndicador"]:
                indicador = laFila["CCODIND"]
                html = laFila["FHTML"]
                if indicador in request.form:
                    result = request.form.get(indicador)
                    if html == "B":
                        result = "1" if result == "on" else "0"
                    if result is not None and result.strip() != "" and result != "null":
                        laDatos.append(
                            {"CCODIND": indicador, "FHTML": html, "CRESULT": result}
                        )
            laData = {
                "CCODACT": session["paData"]["CCODACT"],
                "CTIPSER": session["paData"]["CTIPSER"],
                "CCODPLA": session["paData"]["CCODPLA"],
                "CNRODNI": session["paData"]["CNRODNI"],
                "CNRORUC": session["paData"]["CNRORUC"],
                "CGRABAR": request.form["CGRABAR"],
                "COBSERV": lmObserv,
                "CCONCLU": lmConclu,
                "CRECOME": lmRecome,
                "MCODCIE": session["paCie10"],
                "MDATOS": laDatos,
                "MCODCIE": session["paCie10"],
                "CCODUSU": lcCodUsu,
            }
            loJson = json.dumps(laData)
            llOk = requests.post(
                current_app.config["API_URL"] + "/actividad/detalle", json=loJson
            ).json()
            if not llOk["OK"]:
                raise ValueError(llOk["DATA"])
            return redirect(url_for("Login.main"))
    except Exception as e:
        traceback.print_exc()
        err = str(err)
        flash(err, "error")
    return redirect(url_for("Login.main"))


@Actividad.route("/actividades/<string:pcTipSer>/ZIP", methods=["GET"])
# @login_required
def zip_actividad(pcTipSer):
    try:
        lnIndices = request.form["pnIndice"].split(",")
        len_indice = len(lnIndices)
        if len_indice == 0:
            raise ValueError("NO AH SELECCIONADO NINGUN ITEM")
        import time
        import zipfile

        import BytesIO

        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, "w") as zf:
            for item in lnIndices:
                idx = int(item)
                laData = session["paDatos"][idx]
                location = (
                    current_app.config["PATH_FILE"]
                    + "/"
                    + laData["CNRODNI"]
                    + "/"
                    + laData["CCODACT"]
                    + ".pdf"
                )
                data = zipfile.ZipInfo(location)
                data.date_time = time.localtime(time.time())[:6]
                data.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(data, location)
        memory_file.seek(0)
        return send_file(
            memory_file, attachment_filename=data.date_time + ".zip", as_attachment=True
        )
    except Exception as err:
        print("----------------ERROR-------------------")
        traceback.print_exc()
        err = str(err)
        flash(err, "error")
        return redirect(url_for("Login.main"))


@Actividad.route("/PDF/<string:pcNroDni>/<string:pcCodact>", methods=["GET"])
# @login_required
def pdf_actividad_id(pcNroDni, pcCodact):
    try:
        location = current_app.config["PATH_FILE"] + "/" + pcNroDni
        return send_file(
            location + "/" + pcCodact + ".pdf",
            attachment_filename=pcCodact + ".pdf",
            as_attachment=True,
        )
    except Exception as err:
        print("----------------ERROR-------------------")
        traceback.print_exc()
        err = str(err)
        flash(err, "error")
        return redirect(url_for("Login.main"))


@Actividad.route(
    "/actividades/<string:pcTipSer>/PDF/<string:pnIndice>", methods=["GET"]
)
# @login_required
def pdf_actividad(pcTipSer, pnIndice):
    try:
        laData = session["paDatos"][pnIndice]
        location = current_app.config["PATH_FILE"] + "/" + laData["CNRODNI"]
        return send_file(
            location + "/" + laData["CCODACT"] + ".pdf",
            attachment_filename=laData["CNOMBRE"] + ".pdf",
            as_attachment=True,
        )
    except Exception as err:
        print("----------------ERROR-------------------")
        traceback.print_exc()
        err = str(err)
        flash(err, "error")
        return redirect(url_for("Login.main"))


@Actividad.route("/buscar/cie10/<string:pcParam>", methods=["GET"])
@login_required
def buscararcie10(pcParam):
    try:
        if pcParam.strip() == "":
            raise ValueError("PARAMAETRO DE BUSQUEDA NO DEFINIDO")
        else:
            session["TMP"] = []
            laData = {"CPARAME": pcParam, "CCODUSU": "9999"}
            llOk = requests.get(
                current_app.config["API_URL"] + "/cie10", params=laData
            ).json()
            if not llOk["OK"]:
                raise ValueError(llOk["DATA"])
            session["TMP"] = llOk["DATA"]
            return jsonify(llOk), 200
    except Exception as err:
        traceback.print_exc()
        return abort(400, {"OK": 0, "DATA": str(err)})


@Actividad.route("/agregar/cie10/<int:pnIndice>", methods=["GET", "POST"])
# @login_required
def agregarcie10(pnIndice):
    try:
        found = False
        if session.get("TMP") is not None:
            laData = session["TMP"][pnIndice]
            if session["paCie10"] is not None:
                for laFila in session["paCie10"]:
                    if laData["CCODIGO"] == laFila["CCODIGO"]:
                        found = True
            else:
                session["paCie10"] = []
        if not found:
            if session.get("paCie10") is None:
                session["paCie10"] = []
            session["paCie10"].append(laData)
            return jsonify({"OK": 1, "DATA": session["paCie10"]}), 200
        return abort(400, {"OK": 0, "DATA": "ERROR AL AGREGAR CIE"})
    except Exception as err:
        traceback.print_exc()
        return abort(400, {"OK": 0, "DATA": str(err)})


@Actividad.route("/quitar/cie10/<int:pnIndice>", methods=["POST"])
# @login_required
def quitarcie10(pnIndice):
    try:
        if len(session["paCie10"]) >= pnIndice:
            session["paCie10"].pop(pnIndice)
            return jsonify({"OK": 1, "DATA": session["paCie10"]}), 200
        return abort(400, {"OK": 0, "DATA": "ERROR AL QUITAR CIE"})
    except Exception as err:
        traceback.print_exc()
        return abort(400, {"OK": 0, "DATA": str(err)})


@Actividad.route("/plan/hoja_ruta", methods=["GET"])
@val_session_routes_factory
@login_required
def plan_actividades():
    ploads = {"CCODPLA": session["paData"]["CCODPLA"], "CCODUSU": "9999"}
    llOk = requests.get(
        current_app.config["API_URL"] + "/plan/hoja_ruta", params=ploads
    ).json()
    if not llOk["OK"]:
        return abort(400, {"OK": 0, "DATA": "ERROR AL QUITAR CIE"})
    session["paExamen"] = llOk["DATA"]
    return jsonify({"OK": 1, "DATA": session["paExamen"]}), 200


@Actividad.route("/test", methods=["GET", "POST"])
# @login_required
def codigo_hash():
    try:
        lccodigo = (
            CBase.encrypt(current_app.config["PATH_FILE"] + "/72539751/00019622.pdf")
            or None
        )
        if lccodigo is None:
            raise ValueError("ENCRYPT FALLO")
        return jsonify({"OK": 1, "DATA": lccodigo}), 200
    except Exception as err:
        print(e.__class__.__name__)
        traceback.print_exc()
        return abort(400, {"OK": 0, "DATA": str(err)})


@Actividad.route("/verArchivo", methods=["GET", "POST"])
# @login_required
def ver_archivo_por_codigo():
    try:
        lcCodigo = request.json
        import base64

        location = CBase.decrypt(lcCodigo)
        if not Path(location).is_file():
            raise ValueError("ERROR ARCHIVO NO ENCONTRADO")
        with open(location, "rb") as f:
            loblob = base64.b64encode(f.read())
            return jsonify({"OK": 1, "DATA": loblob}), 200
    except Exception as err:
        print(e.__class__.__name__)
        traceback.print_exc()
        return abort(400, {"OK": 0, "DATA": str(err)})
