from flask import Flask, render_template, request
from datetime import datetime

from config import Config
from services.weather_service import get_coordinates, get_trip_weather
from services.packing_engine import generate_packing_list
from services.llm_service import ask_ai

app = Flask(__name__)
app.config.from_object(Config)

# Activity options available on the form
ACTIVITY_CHOICES = {
    "A": "City sightseeing",
    "B": "Hiking or outdoor excursions",
    "C": "Business meetings or formal events",
    "D": "Sports (Gym/Volleyball)",
    "E": "Beach or pool vacation"
}


@app.route("/", methods=["GET", "POST"])
def index():
    """Homepage with trip form."""
    if request.method == "POST":
        destination = request.form.get("destination")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        activities = request.form.getlist("activities")

        # Convert string → datetime
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(end_date, "%Y-%m-%d")

        # Weather API: get coordinates
        lat, lon = get_coordinates(destination)

        weather_data = None
        packing_list = None

        if lat and lon:
            weather_data = get_trip_weather(lat, lon, start_dt, end_dt)

            trip_length = (end_dt - start_dt).days + 1

            # Create packing list
            packing_list = generate_packing_list(
                trip_length=trip_length,
                weather_data=weather_data,
                activities=activities
            )

        return render_template(
            "results.html",
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            weather=weather_data,
            packing_list=packing_list,
            activities=activities,
            ai_answer=None
        )

    return render_template("index.html", activities=ACTIVITY_CHOICES)


@app.route("/ask_ai", methods=["POST"])
def ask_ai_route():
    """User submits a question to OpenAI."""
    user_question = request.form.get("user_question")
    ai_answer = ask_ai(user_question)

    # Re-render results page WITH the AI response included
    return render_template(
        "results.html",
        destination=request.form.get("destination"),
        start_date=request.form.get("start_date"),
        end_date=request.form.get("end_date"),
        weather=None,                 # Results page will ignore None
        packing_list=None,            # Same here
        activities=None,
        ai_answer=ai_answer
    )


if __name__ == "__main__":
    app.run(debug=True)
