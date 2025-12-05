import math
from config import TEMP_HOT, TEMP_COLD

def generate_packing_list(days, weather_profile, activities):
    """
    Generates a dictionary of packing items based on rules.
    """
    # 1. Base Essentials (Rule: Scale with days)
    # Re-wear rule: 1 shirt every 2 days
    shirts = math.ceil(days / 2)
    pants = math.ceil(days / 3)
    
    packing_list = {
        "Clothing": {
            "Underwear": days,
            "Socks": days,
            "T-Shirts/Tops": max(2, shirts),
            "Pants/Bottoms": max(1, pants),
            "Sleepwear": 1,
            "Casual Shoes": 1
        },
        "Toiletries": {
            "Toothbrush & Paste": 1,
            "Deodorant": 1,
            "Shampoo/Soap": 1
        },
        "Electronics": {
            "Phone Charger": 1,
            "Power Bank": 1
        },
        "Optional": {}
    }

    # 2. Weather Rules
    if weather_profile['is_cold']:
        packing_list["Clothing"]["Heavy Coat"] = 1
        packing_list["Clothing"]["Thermal Layers"] = 2
        packing_list["Clothing"]["Beanie/Gloves"] = 1
    elif weather_profile['avg_temp_max'] > TEMP_HOT:
        packing_list["Clothing"]["Shorts"] = 2
        packing_list["Optional"]["Sunscreen"] = 1
        packing_list["Optional"]["Sunglasses"] = 1

    if weather_profile['is_rainy']:
        packing_list["Clothing"]["Rain Jacket"] = 1
        packing_list["Optional"]["Umbrella"] = 1

    # 3. Activity Rules
    if 'B' in activities: # Hiking
        packing_list["Clothing"]["Hiking Boots"] = 1
        packing_list["Optional"]["Bug Spray"] = 1
        packing_list["Clothing"]["Moisture-wicking socks"] = 2
    
    if 'C' in activities: # Business
        packing_list["Clothing"]["Formal Suit/Dress"] = 1
        packing_list["Clothing"]["Dress Shoes"] = 1
        
    if 'E' in activities: # Beach
        packing_list["Clothing"]["Swimsuit"] = 1
        packing_list["Optional"]["Beach Towel"] = 1
        packing_list["Clothing"]["Sandals/Flip-flops"] = 1

    # International Travel Check (General rule for Europe context)
    packing_list["Electronics"]["Travel Adapter"] = 1 

    return packing_list