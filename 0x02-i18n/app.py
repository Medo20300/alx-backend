#!/usr/bin/env python3
"""
A Basic Flask application
"""
import pytz
import datetime
from typing import Dict, Union
from flask import Flask, g, request, render_template
from flask_babel import Babel, format_datetime

class Config(object):
    """
    Application configuration class
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'

# Instantiate the application object
app = Flask(__name__)
app.config.from_object(Config)

# Wrap the application with Babel
babel = Babel(app)

# Sample user data
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "en", "timezone": "Vulcan"},  # Fixed locale
    4: {"name": "Teletubby", "locale": "en", "timezone": "Europe/London"},  # Fixed locale
}

def get_user(id) -> Union[Dict[str, Union[str, None]], None]:
    """
    Validate user login details
    Args:
        id (str): user id
    Returns:
        (Dict): user dictionary if id is valid else None
    """
    return users.get(int(id), None)

def get_locale() -> str:
    """
    Gets locale from request object
    """
    options = [
        request.args.get('locale', '').strip(),
        g.user.get('locale', None) if g.user else None,
        request.accept_languages.best_match(app.config['LANGUAGES']),
        Config.BABEL_DEFAULT_LOCALE
    ]
    for locale in options:
        if locale in Config.LANGUAGES:
            return locale
    return Config.BABEL_DEFAULT_LOCALE

def get_timezone() -> str:
    """
    Gets timezone from request object
    """
    tz = request.args.get('timezone', '').strip()
    if not tz and g.user:
        tz = g.user.get('timezone', app.config['BABEL_DEFAULT_TIMEZONE'])
    try:
        tz = pytz.timezone(tz).zone
    except pytz.UnknownTimeZoneError:
        tz = app.config['BABEL_DEFAULT_TIMEZONE']
    return tz

@app.before_request
def before_request() -> None:
    """
    Adds valid user to the global session object `g`
    """
    user_id = request.args.get('login_as', None)
    if user_id:
        g.user = get_user(user_id)
    else:
        g.user = None
    g.locale = get_locale()
    g.timezone = get_timezone()
    g.time = format_datetime(datetime.datetime.now(pytz.timezone(g.timezone)))

@app.route('/', strict_slashes=False)
def index() -> str:
    """
    Renders a basic html template
    """
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
