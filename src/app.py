from os import environ
from flask import Flask
from waitress import serve
from controllers.recipes_controller import recipes_controller

app = Flask(__name__)

app.register_blueprint(recipes_controller, url_prefix="/recipes")

def start_server(host: str = "127.0.0.1", port: int = 8080):
    if environ.get("FLASK_ENV") == "dev":
        return app.run(debug=True, host=host, port=port)
    else:
        serve(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
