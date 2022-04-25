import functools

from flask import current_app, redirect, request, session, url_for


def login_required(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if current_app.config["SECURE"]:
            if "CCODUSU" not in session:
                return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return secure_function


def val_session_routes_factory(func):
    @functools.wraps(func)
    def secure_function(*args, **kwargs):
        if current_app.config["SECURE"]:
            if request.path not in session["ROUTES"]:
                return redirect(url_for("login", next=request.url))
        return func(*args, **kwargs)

    return secure_function


def exception_handler_request(func) -> object:
    @functools.wraps(func)
    def inner_function(*args, **kwargs):
        R1 = {"OK": 0, "DATA": ""}
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("-" * 60)
            print(e.__class__.__name__)
            traceback.print_exc()
            print("-" * 60)
            if e.__class__.__name__ in [
                "ValueError",
                "AssertionError",
                "KeyError",
                "TypeError",
            ]:
                R1["DATA"] = str(e)
                return jsonify(R1), 400
            else:
                R1["DATA"] = str(e)
                return jsonify(R1), 500

    return inner_function


# def val_session_routes_factory(opc):
#     def val_session_routes(function):
#         def wrapper(*args, **kwargs):
#             if opc not in session['ROUTES']:
#                 return redirect(url_for("login", next=request.url))
#             result = function(*args, **kwargs)
#             return result
#         return wrapper
#     return val_session_routes
