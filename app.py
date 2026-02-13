from flask import Flask
from models import db
from api import api
from frontend import frontend

app = Flask(__name__)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///rbac.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Init DB
db.init_app(app)

# Register blueprints
app.register_blueprint(api)
app.register_blueprint(frontend)

# Create tables
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    print("Starting RBAC app on http://127.0.0.1:5000/roles")
    app.run(debug=True)
