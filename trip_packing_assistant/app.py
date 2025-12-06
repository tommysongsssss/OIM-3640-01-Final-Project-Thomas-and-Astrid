from flask import Flask, render_template, request
from datetime import datetime

from config import Config
from services.weather_service import get_coordinates, get_trip_weather
from services.packing_engine import generate_packing_list
from services.llm_service import ask_ai

app = Flask(__name__)
app.config.from_object(Config)

# Activity choices shown on the form
ACTIVITY_CHOICES = {
   "A": "City sightseeing",
    "B": "Hiking or outdoor excursions",
    "C": "Business meetings or formal events",
    "D": "Sports (Gym/Volleyball)",
    "E": "Beach or pool vacation",
    "F": "Nightlife / Clubs",
    "G": "Photography / Content creation",
    "H": "Long travel days (airport, train, etc.)",
    "I": "Rainy-day indoor activities",
    "J": "Luxury dining or upscale events"
}


@app.route("/", methods=["GET", "POST"])
def index():
    """Homepage: form for trip details."""
    if request.method == "POST":
        destination = request.form.get("destination")
        start_date_str = request.form.get("start_date")
        end_date_str = request.form.get("end_date")
        activities = request.form.getlist("activities")

        # Convert strings → datetime objects
        start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date_str, "%Y-%m-%d")
        trip_length = (end_dt - start_dt).days + 1

        # Get coordinates + weather
        lat, lon = get_coordinates(destination)
        weather_data = None
        packing_list = None

        if lat is not None and lon is not None:
            weather_data = get_trip_weather(lat, lon, start_dt, end_dt)
            packing_list = generate_packing_list(trip_length, weather_data, activities)

        return render_template(
            "results.html",
            destination=destination,
            start_date=start_date_str,
            end_date=end_date_str,
            activities=activities,
            weather=weather_data,
            packing_list=packing_list,
            ai_answer=None
        )

    return render_template("index.html", activities=ACTIVITY_CHOICES)


@app.route("/ask_ai", methods=["POST"])
def ask_ai_route():
    """
    Handle 'Ask AI' form on results page.
    We recompute weather + packing so the page stays consistent.
    """
    user_question = request.form.get("user_question")

    destination = request.form.get("destination")
    start_date_str = request.form.get("start_date")
    end_date_str = request.form.get("end_date")
    activities_str = request.form.get("activities", "")
    activities = activities_str.split(",") if activities_str else []

    # Recompute trip info for consistency
    start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date_str, "%Y-%m-%d")
    trip_length = (end_dt - start_dt).days + 1

    lat, lon = get_coordinates(destination)
    weather_data = None
    packing_list = None

    if lat is not None and lon is not None:
        weather_data = get_trip_weather(lat, lon, start_dt, end_dt)
        packing_list = generate_packing_list(trip_length, weather_data, activities)

    # Build human-readable context for the model
    activity_labels = [ACTIVITY_CHOICES.get(a, a) for a in activities]
    context = (
        f"Destination: {destination}, dates: {start_date_str} to {end_date_str}. "
        f"Activities: {', '.join(activity_labels) if activity_labels else 'not specified'}."
    )

    ai_answer = ask_ai(user_question, context)

    return render_template(
        "results.html",
        destination=destination,
        start_date=start_date_str,
        end_date=end_date_str,
        activities=activities,
        weather=weather_data,
        packing_list=packing_list,
        ai_answer=ai_answer
    )


if __name__ == "__main__":
    app.run(debug=True)