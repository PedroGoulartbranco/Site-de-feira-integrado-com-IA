from flask import Flask
from views.routes import views_bp
import os

app = Flask(__name__)

app.register_blueprint(views_bp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)