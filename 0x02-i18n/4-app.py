#!/usr/bin/env python3
"""Module for task 4
"""
from flask import Flask, render_template, request
from flask_babel import Babel

app = Flask(__name__)

app.url_map.strict_slashes = False

class Config:
    """Represents a Flask Babel configuration."""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"

app.config.from_object(Config)
babel = Babel(app)

@babel.localeselector
def get_locale() -> str:
    """Determines the best match for the client's preferred language."""
    locale = request.args.get('locale', None)
    supported_languages = app.config["LANGUAGES"]
    if locale and locale in supported_languages:
        return locale
    return request.accept_languages.best_match(supported_languages)

@app.route("/")
def index_4() -> str:
    """The index function displays the home page of the web application.

    Returns:
        str: contents of the home page.
    """
    return render_template("4-index.html")

if __name__ == "__main__":
    app.run(debug=True)
