def generate_packing_list(trip_length, weather_data, activities):
    """
    Simple rule-based packing engine using weather and activities.
    """

    packing = {}

    # Basic clothing
    packing["Shirts"] = max(3, trip_length // 2)
    packing["Pants"] = max(2, trip_length // 3)
    packing["Underwear"] = trip_length
    packing["Socks"] = trip_length

    # --- Weather-based logic ---
    avg_temp = weather_data.get("avg_temp_max")
    max_pop = weather_data.get("max_pop", 0)

    # Cold weather
    if avg_temp is not None and avg_temp < 10:
        packing["Warm Jacket"] = 1
        packing["Thermal Layers"] = 2

    # Hot weather
    if avg_temp is not None and avg_temp > 25:
        packing["Light T-Shirts"] = 2
        packing["Shorts"] = 1

    # Rainy conditions
    if max_pop > 0.4:
        packing["Rain Jacket"] = 1

    # Activity-based
    if "B" in activities:  # Hiking
        packing["Hiking Boots"] = 1
        packing["Water Bottle"] = 1

    if "E" in activities:  # Beach
        packing["Swimsuit"] = 1
        packing["Sunscreen"] = 1
        packing["Flip-Flops"] = 1

    if "C" in activities:  # Business
        packing["Formal Outfit"] = 1
        packing["Dress Shoes"] = 1

    return packing
