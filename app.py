from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect
from datetime import datetime

import random, string

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///spots.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)

class Spot(db.Model):
    id = db.Column(db.String(5),primary_key=True)
    Vehicle_no = db.Column(db.String(10))

    def __repr__(self) -> str:
        return f"{self.id} {self.Vehicle_no}"

with app.app_context():
    db.create_all()

@app.route("/", methods=["POST","GET"])
def index():
    if request.method == "POST":
        vehicle_no = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        spot = Spot.query.filter_by(id=request.form["spots"]).first()        
        spot.Vehicle_no = vehicle_no
        db.session.commit()
        return redirect("/parked")
    spots = Spot.query.all()
    return render_template("index.html",spots=spots)

@app.route("/parked")
def parked():
    return "Parked"

@app.route("/clear/<string:id>")
def clear(id):
    spot = Spot.query.filter_by(id=id).first()
    spot.Vehicle_no = None
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)