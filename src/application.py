"""
    GONE WITH THE WIND:
    an application that get weather and movies data
"""

from os import environ
from logging import getLogger, basicConfig
from sanic import Sanic
from sanic.response import json
from weather import blueprint as weather_blueprint
from movies import blueprint as movies_blueprint

# setup loging level
basicConfig(level=environ.get("LOGLEVEL", "INFO"))

logger = getLogger(__name__)
app = Sanic("gone with the wind")
app.blueprint(weather_blueprint)
app.blueprint(movies_blueprint)

@app.route("/version")
def version(_):
    return json({'version': '1.0.0'})

# static route for the main application
app.static('/', './static/index.html', content_type="text/html; charset=utf-8")

if __name__ == "__main__":
    port = int(environ.get("PORT", "8080"))
    debug_mode = "DEBUG" in environ
    app.run(debug=debug_mode, auto_reload=True)
