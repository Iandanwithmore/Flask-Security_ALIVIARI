import traceback

import rsa
from flask import current_app


class CBase:
    def __init__(self):
        self.error = None

    @staticmethod
    def encrypt(txt: str) -> str:
        codigo = None
        try:
            encode = bytes(txt, "latin-1")
            codigo = rsa.encrypt(encode, current_app.config["RSA_PUBLIC"]).decode(
                "latin-1"
            )
            # decode=rsa.decrypt(bytes(codigo,"latin-1"), current_app.config["RSA_PRIVATE"])
            # print(type(decode))
            # print(decode)
        except Exception:
            traceback.print_exc()
        return codigo

    @staticmethod
    def decrypt(txt: str) -> str:
        codigo = None
        try:
            decode = bytes(txt, "latin-1")
            codigo = rsa.decrypt(decode, current_app.config["RSA_PRIVATE"]).decode(
                "latin-1"
            )
            # print(type(codigo))
            # print(codigo)
        except Exception:
            traceback.print_exc()
        return codigo
