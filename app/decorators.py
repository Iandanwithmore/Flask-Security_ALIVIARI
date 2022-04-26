import functools
import inspect
import traceback

from flask import current_app, flash, redirect, request, session, url_for


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


def exception_handler(error_response):
    def factory_exception(func):
        @functools.wraps(func)
        def inner_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print("-" * 60)
                print(f"CALLER: {inspect.stack()[1][2]}-{inspect.stack()[1][3]}()")
                print(e.__class__.__name__)
                traceback.print_exc()
                print("-" * 60)
                if e.__class__.__name__ in [
                    "ValueError",
                    "AssertionError",
                    "KeyError",
                    "TypeError",
                ]:
                    flash(str(e), "error")
                    return redirect(url_for(error_response))

        return inner_function

    return factory_exception