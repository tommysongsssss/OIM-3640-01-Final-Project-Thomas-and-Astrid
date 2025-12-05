from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from config import Config, ACTIVITY_CHOICES
from services.weather_service import get_coordinates, get_trip_weather
from services.packing_engine import generate_packing_list
from services.llm_service import get_ai_outfit_recommendation

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        destination = request.form.get('destination')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        activities = request.form.getlist('activities')

        if not destination or not start_date or not end_date:
            flash("Please fill in all fields.")
            return redirect(url_for('index'))

        # Pass data to results route via query params
        return redirect(url_for('results', 
                                dest=destination, 
                                start=start_date, 
                                end=end_date, 
                                acts=','.join(activities)))

    return render_template('index.html', activities=ACTIVITY_CHOICES)

@app.route('/results')
def results():
    destination = request.args.get('dest')
    start_str = request.args.get('start')
    end_str = request.args.get('end')
    activities = request.args.get('acts', '').split(',')

    try:
        # 1. Parse Dates
        start_date = datetime.strptime(start_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_str, '%Y-%m-%d')
        trip_length = (end_date - start_date).days + 1

        # 2. Get Weather Data
        lat, lon = get_coordinates(destination)
        if lat is None:
            flash(f"Could not find location: {destination}")
            return redirect(url_for('index'))

        weather_data = get_trip_weather(lat, lon, start_date, end_date)

        # 3. Generate Packing List
        packing_list = generate_packing_list(trip_length, weather_data, activities)

        # 4. (Optional) Get AI Outfit Recommendation
        # We pass a summary string to the LLM service
        weather_summary = f"Trip to {destination}. Highs around {weather_data['avg_temp_max']}C, Rain chance {weather_data['max_pop']*100}%."
        ai_suggestion = get_ai_outfit_recommendation(weather_summary, activities)

        return render_template('results.html', 
                               destination=destination,
                               trip_length=trip_length,
                               weather=weather_data,
                               packing_list=packing_list,
                               ai_suggestion=ai_suggestion)

    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred processing your trip. Please try again.")
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)