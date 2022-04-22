from app import create_app
from app.config import DevelopmentConfig, ProductionConfig, TestingConfig
from flask import render_template, url_for
from flask_session import Session

# import the application config classes
from waitress import serve

app = create_app()

server_session = Session()
server_session.init_app(app)


@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def not_found(error):
    return render_template("error/error.html", code="400", msg=error)


# favicon
@app.route("/favicon.ico")
def favicon():
    return url_for("static", filename="/svg/logo.svg")


if __name__ == "__main__":
    # app.run(debug=True, port=app.config["APP_PORT"], threaded=True)
    serve(app, host="0.0.0.0", port=app.config["APP_PORT"])
