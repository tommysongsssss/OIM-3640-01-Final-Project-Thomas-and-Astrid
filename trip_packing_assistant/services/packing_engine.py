def generate_packing_list(trip_length, weather_data, activities):
    """
    Enhanced rule-based packing engine using weather, activities, and trip length.
    Keeps all original logic but adds smarter, more realistic packing suggestions.
    """

    packing = {}

    # -----------------------
    # Basic Clothing (yours)
    # -----------------------
    packing["Shirts"] = max(3, trip_length // 2)
    packing["Pants"] = max(2, trip_length // 3)
    packing["Underwear"] = trip_length
    packing["Socks"] = trip_length

    # Weather inputs
    avg_temp = weather_data.get("avg_temp_max")
    max_pop = weather_data.get("max_pop", 0)

    # -----------------------
    # Weather-Based Logic
    # -----------------------

    # Very cold
    if avg_temp is not None and avg_temp < 5:
        packing["Heavy Coat"] = 1
        packing["Thermal Layers"] = 2
        packing["Scarf"] = 1
        packing["Gloves"] = 1
        packing["Beanie"] = 1

    # Your original cold rule
    elif avg_temp is not None and avg_temp < 10:
        packing["Warm Jacket"] = 1
        packing["Thermal Layers"] = 2

    # Mild weather 10–20°C
    if avg_temp is not None and 10 <= avg_temp <= 20:
        packing["Light Jacket"] = 1
        packing["Long Sleeves"] = 2

    # Your original hot rule + expansion
    if avg_temp is not None and avg_temp > 25:
        packing["Light T-Shirts"] = 2
        packing["Shorts"] = 1
        packing["Sunglasses"] = 1
        packing["Sun Hat"] = 1

    # Rain logic (yours + expansion)
    if max_pop > 0.4:
        packing["Rain Jacket"] = 1
        packing["Umbrella"] = 1
        packing["Waterproof Bag Cover"] = 1

    # -----------------------
    # Activity-Based Logic
    # -----------------------

    # B = Hiking
    if "B" in activities:
        packing["Hiking Boots"] = 1
        packing["Water Bottle"] = 1
        packing["Daypack"] = 1
        packing["Extra Socks"] = 2

    # E = Beach
    if "E" in activities:
        packing["Swimsuit"] = 1
        packing["Sunscreen"] = 1
        packing["Flip-Flops"] = 1
        packing["Beach Towel"] = 1
        packing["After-Sun Lotion"] = 1

    # C = Business
    if "C" in activities:
        packing["Formal Outfit"] = 1
        packing["Dress Shoes"] = 1
        packing["Blazer"] = 1
        packing["Notebook"] = 1

    # -----------------------
    # Trip-Length Logic
    # -----------------------
    if trip_length > 7:
        packing["Laundry Detergent Sheets"] = 1
        packing["Extra Shirt"] = 1

    if trip_length > 10:
        packing["Extra Pants"] = 1

    # -----------------------
    # Universal Essentials
    # -----------------------
    packing["Toiletries Kit"] = 1
    packing["Charging Cable"] = 1
    packing["Travel Adapter"] = 1
    packing["Portable Charger"] = 1
 # F = Nightlife / Partying
    if "F" in activities:
        packing["Going-Out Outfit"] = 1
        packing["Fragrance / Cologne"] = 1

    # G = Photography / Content creation
    if "G" in activities:
        packing["Camera"] = 1
        packing["Tripod"] = 1
        packing["Extra SD Card"] = 1
        packing["Power Bank"] = 1

    # H = Snow Sports / Ski Trip
    if "H" in activities:
        packing["Ski Jacket"] = 1
        packing["Ski Pants"] = 1
        packing["Gloves"] = 1
        packing["Neck Warmer"] = 1
        packing["Thermal Socks"] = 2

    # I = Long-Haul Flight
    if "I" in activities:
        packing["Neck Pillow"] = 1
        packing["Compression Socks"] = 1
        packing["Travel Blanket"] = 1
        packing["Earplugs"] = 1

    # J = Shopping Trip
    if "J" in activities:
        packing["Foldable Bag"] = 1
        packing["Extra Budget Space"] = 1
        
    return packing