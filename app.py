from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configure the database URI
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///satellite.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Define the Satellite model
class Satellite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    continent = db.Column(db.String(50), nullable=False)
    satellite_type = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    manufacturer = db.Column(db.String(50), nullable=False)

# Create the database and tables if they don't exist
with app.app_context():
    if not os.path.exists("satellite.db"):
        db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Capture form data
        continent = request.form.get("continent")
        satellite_type = request.form.get("satellite_type")
        cost = request.form.get("cost")
        manufacturer = request.form.get("manufacturer")

        # Create a new Satellite record
        new_satellite = Satellite(
            continent=continent,
            satellite_type=satellite_type,
            cost=cost,
            manufacturer=manufacturer
        )
        db.session.add(new_satellite)
        db.session.commit()

        return redirect(url_for("index"))

    # Query all satellite records
    satellites = Satellite.query.all()
    return render_template("index.html", satellites=satellites)

if __name__ == "__main__":
    app.run(debug=True)


