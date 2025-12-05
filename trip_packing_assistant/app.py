from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from config import ACTIVITY_CHOICES
from services.weather_service import get_coordinates, get_trip_weather
from services.packing_engine import generate_packing_list

app = Flask(__name__)
app.secret_key = "simple-project-key"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        dest = request.form.get("destination")
        start = request.form.get("start_date")
        end = request.form.get("end_date")
        activities = request.form.getlist("activities")

        if not dest or not start or not end:
            flash("Please fill in all fields.")
            return redirect(url_for("index"))

        return redirect(url_for("results",
            dest=dest,
            start=start,
            end=end,
            acts=",".join(activities)
        ))

    return render_template("index.html", activities=ACTIVITY_CHOICES)


@app.route("/results")
def results():
    dest = request.args.get("dest")
    start_str = request.args.get("start")
    end_str = request.args.get("end")
    acts = request.args.get("acts", "").split(",")

    start = datetime.strptime(start_str, "%Y-%m-%d")
    end = datetime.strptime(end_str, "%Y-%m-%d")
    trip_len = (end - start).days + 1

    lat, lon = get_coordinates(dest)
    if lat is None:
        flash("Location not found.")
        return redirect(url_for("index"))

    weather = get_trip_weather(lat, lon, start, end)
    packing = generate_packing_list(trip_len, weather, acts)

    return render_template("results.html",
                           destination=dest,
                           trip_length=trip_len,
                           weather=weather,
                           packing_list=packing)


if __name__ == "__main__":
    app.run(debug=True)
