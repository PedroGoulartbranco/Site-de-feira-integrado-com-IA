from flask import Flask
from views.routes import views_bp

app = Flask(__name__)

app.register_blueprint(views_bp)

if __name__ == "__main__":
    app.run()